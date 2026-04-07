"""
PersonaAI Advanced API Integration Module
==========================================
Integrates with multiple APIs for real-world recommendation data:
- TMDb API for movies
- Spotify API for music
- News API for articles
- GraphQL endpoints
"""

import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

class APIConfig:
    """API Configuration and constants"""
    
    # TMDb Configuration
    TMDB_BASE_URL = "https://api.themoviedb.org/3"
    TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"
    
    # Spotify Configuration
    SPOTIFY_BASE_URL = "https://api.spotify.com/v1"
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"
    
    # News API
    NEWS_API_BASE = "https://newsapi.org/v2"
    
    # Cache duration (seconds)
    CACHE_DURATION = 3600


class APIKeyManager:
    """Secure API key management"""
    
    def __init__(self):
        self.keys = {
            'tmdb': os.getenv('TMDB_API_KEY', 'demo_key'),
            'spotify_id': os.getenv('SPOTIFY_CLIENT_ID', 'demo_id'),
            'spotify_secret': os.getenv('SPOTIFY_CLIENT_SECRET', 'demo_secret'),
            'news': os.getenv('NEWS_API_KEY', 'demo_key'),
        }
    
    def get_key(self, service: str) -> str:
        """Safely retrieve API key"""
        key = self.keys.get(service)
        if not key or key.startswith('demo'):
            logger.warning(f"Using demo key for {service}")
        return key


# ============================================================================
# MOVIE RECOMMENDATIONS (TMDB)
# ============================================================================

class TMDbClient:
    """TMDb API Client for movie recommendations"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = APIConfig.TMDB_BASE_URL
        self.session = requests.Session()
        self.session.params = {'api_key': api_key}
    
    @lru_cache(maxsize=100)
    def search_movies(self, query: str, year: Optional[int] = None) -> List[Dict]:
        """
        Search for movies
        
        Args:
            query: Movie title to search
            year: Optional release year filter
        
        Returns:
            List of movie results
        """
        try:
            params = {'query': query, 'language': 'en-US'}
            if year:
                params['year'] = year
            
            response = self.session.get(
                f"{self.base_url}/search/movie",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            results = response.json().get('results', [])
            
            return [{
                'id': r['id'],
                'title': r['title'],
                'release_date': r.get('release_date', ''),
                'rating': r.get('vote_average', 0),
                'overview': r.get('overview', ''),
                'poster_path': r.get('poster_path'),
                'popularity': r.get('popularity', 0),
                'genre_ids': r.get('genre_ids', []),
            } for r in results[:10]]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb search error: {e}")
            return []
    
    def get_movie_details(self, movie_id: int) -> Dict:
        """
        Get detailed information about a movie
        
        Args:
            movie_id: TMDb movie ID
        
        Returns:
            Detailed movie information
        """
        try:
            response = self.session.get(
                f"{self.base_url}/movie/{movie_id}",
                params={'append_to_response': 'credits,recommendations'},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                'id': data['id'],
                'title': data['title'],
                'rating': data.get('vote_average', 0),
                'runtime': data.get('runtime', 0),
                'genres': [g['name'] for g in data.get('genres', [])],
                'director': next(
                    (c['name'] for c in data.get('credits', {}).get('crew', []) if c['job'] == 'Director'),
                    'Unknown'
                ),
                'cast': [c['name'] for c in data.get('credits', {}).get('cast', [])[:5]],
                'overview': data.get('overview', ''),
                'release_date': data.get('release_date', ''),
                'budget': data.get('budget', 0),
                'revenue': data.get('revenue', 0),
                'recommendations': [{
                    'id': r['id'],
                    'title': r['title'],
                    'rating': r.get('vote_average', 0)
                } for r in data.get('recommendations', {}).get('results', [])[:5]]
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb details error: {e}")
            return {}
    
    def get_trending_movies(self, time_window: str = 'week') -> List[Dict]:
        """
        Get trending movies
        
        Args:
            time_window: 'day' or 'week'
        
        Returns:
            List of trending movies
        """
        try:
            response = self.session.get(
                f"{self.base_url}/trending/movie/{time_window}",
                timeout=10
            )
            response.raise_for_status()
            results = response.json().get('results', [])
            
            return [{
                'id': r['id'],
                'title': r['title'],
                'rating': r.get('vote_average', 0),
                'poster_path': r.get('poster_path'),
                'overview': r.get('overview', ''),
                'popularity': r.get('popularity', 0),
                'trend_score': r.get('vote_count', 0) * r.get('vote_average', 0) / 100
            } for r in results[:20]]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb trending error: {e}")
            return []
    
    def get_recommendations(self, movie_id: int, n: int = 10) -> List[Dict]:
        """
        Get movies recommended based on a given movie
        
        Args:
            movie_id: Reference movie ID
            n: Number of recommendations
        
        Returns:
            List of recommended movies
        """
        try:
            response = self.session.get(
                f"{self.base_url}/movie/{movie_id}/recommendations",
                params={'page': 1},
                timeout=10
            )
            response.raise_for_status()
            results = response.json().get('results', [])
            
            return [{
                'id': r['id'],
                'title': r['title'],
                'rating': r.get('vote_average', 0),
                'poster_path': r.get('poster_path'),
                'overview': r.get('overview', '')
            } for r in results[:n]]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb recommendations error: {e}")
            return []


# ============================================================================
# MUSIC RECOMMENDATIONS (SPOTIFY)
# ============================================================================

class SpotifyClient:
    """Spotify API Client for music recommendations"""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = APIConfig.SPOTIFY_BASE_URL
        self.access_token = None
        self.token_expires = None
        self._refresh_token()
    
    def _refresh_token(self):
        """Refresh Spotify access token"""
        try:
            auth = (self.client_id, self.client_secret)
            data = {'grant_type': 'client_credentials'}
            
            response = requests.post(
                APIConfig.SPOTIFY_AUTH_URL,
                auth=auth,
                data=data,
                timeout=10
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.token_expires = datetime.now() + timedelta(seconds=token_data['expires_in'])
            
            logger.info("Spotify token refreshed")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Spotify authentication error: {e}")
            self.access_token = None
    
    def _get_headers(self) -> Dict:
        """Get request headers with authentication"""
        if not self.access_token:
            self._refresh_token()
        
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def search_tracks(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for tracks
        
        Args:
            query: Track or artist name
            limit: Number of results
        
        Returns:
            List of tracks
        """
        try:
            params = {
                'q': query,
                'type': 'track',
                'limit': min(limit, 50)
            }
            
            response = requests.get(
                f"{self.base_url}/search",
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            tracks = response.json().get('tracks', {}).get('items', [])
            return [{
                'id': t['id'],
                'name': t['name'],
                'artist': t['artists'][0]['name'] if t['artists'] else 'Unknown',
                'album': t['album']['name'],
                'popularity': t.get('popularity', 0),
                'duration_ms': t.get('duration_ms', 0),
                'release_date': t['album'].get('release_date', ''),
                'preview_url': t.get('preview_url'),
                'image': t['album']['images'][0]['url'] if t['album']['images'] else None
            } for t in tracks]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Spotify search error: {e}")
            return []
    
    def get_recommendations(self, seed_artists: List[str] = None, 
                          seed_genres: List[str] = None,
                          seed_tracks: List[str] = None,
                          limit: int = 10) -> List[Dict]:
        """
        Get recommendations based on seeds
        
        Args:
            seed_artists: List of artist IDs
            seed_genres: List of genre names
            seed_tracks: List of track IDs
            limit: Number of recommendations
        
        Returns:
            List of recommended tracks
        """
        try:
            params = {'limit': min(limit, 100)}
            
            if seed_artists:
                params['seed_artists'] = ','.join(seed_artists[:5])
            if seed_genres:
                params['seed_genres'] = ','.join(seed_genres[:5])
            if seed_tracks:
                params['seed_tracks'] = ','.join(seed_tracks[:5])
            
            response = requests.get(
                f"{self.base_url}/recommendations",
                headers=self._get_headers(),
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            tracks = response.json().get('tracks', [])
            return [{
                'id': t['id'],
                'name': t['name'],
                'artist': t['artists'][0]['name'] if t['artists'] else 'Unknown',
                'album': t['album']['name'],
                'popularity': t.get('popularity', 0),
                'preview_url': t.get('preview_url'),
                'image': t['album']['images'][0]['url'] if t['album']['images'] else None,
                'danceability': t.get('danceability', 0),
                'energy': t.get('energy', 0),
                'valence': t.get('valence', 0)
            } for t in tracks]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Spotify recommendations error: {e}")
            return []


# ============================================================================
# NEWS RECOMMENDATIONS
# ============================================================================

class NewsAPIClient:
    """News API Client for article recommendations"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = APIConfig.NEWS_API_BASE
    
    def search_articles(self, query: str, language: str = 'en', 
                       sort_by: str = 'relevancy', limit: int = 10) -> List[Dict]:
        """
        Search for news articles
        
        Args:
            query: Search query
            language: Language code
            sort_by: 'relevancy', 'popularity', 'publishedAt'
            limit: Number of articles
        
        Returns:
            List of articles
        """
        try:
            params = {
                'q': query,
                'language': language,
                'sortBy': sort_by,
                'pageSize': min(limit, 100),
                'apiKey': self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/everything",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            return [{
                'title': a['title'],
                'description': a.get('description', ''),
                'source': a['source']['name'],
                'url': a['url'],
                'image': a.get('urlToImage'),
                'published_at': a.get('publishedAt', ''),
                'author': a.get('author', 'Unknown'),
                'content': a.get('content', '')
            } for a in articles]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"News API search error: {e}")
            return []
    
    def get_top_headlines(self, category: str = 'general', 
                         country: str = 'us', limit: int = 10) -> List[Dict]:
        """
        Get top headlines
        
        Args:
            category: News category
            country: Country code
            limit: Number of articles
        
        Returns:
            List of top headlines
        """
        try:
            params = {
                'category': category,
                'country': country,
                'pageSize': min(limit, 100),
                'apiKey': self.api_key
            }
            
            response = requests.get(
                f"{self.base_url}/top-headlines",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            articles = response.json().get('articles', [])
            return [{
                'title': a['title'],
                'description': a.get('description', ''),
                'source': a['source']['name'],
                'url': a['url'],
                'image': a.get('urlToImage'),
                'published_at': a.get('publishedAt', ''),
                'content': a.get('content', '')
            } for a in articles]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"News API headlines error: {e}")
            return []


# ============================================================================
# ASYNC API ORCHESTRATOR
# ============================================================================

class AsyncAPIOrchestrator:
    """Orchestrates multiple API calls asynchronously"""
    
    def __init__(self, api_config: Dict):
        self.tmdb = TMDbClient(api_config.get('tmdb'))
        self.spotify = SpotifyClient(
            api_config.get('spotify_id'),
            api_config.get('spotify_secret')
        )
        self.news = NewsAPIClient(api_config.get('news'))
    
    async def fetch_all_recommendations(self, 
                                       movie_query: str = None,
                                       music_query: str = None,
                                       news_query: str = None) -> Dict:
        """
        Fetch recommendations from all sources asynchronously
        
        Returns:
            Dictionary with recommendations from each API
        """
        results = {}
        
        tasks = []
        
        if movie_query:
            tasks.append(self._async_movie_search(movie_query))
        if music_query:
            tasks.append(self._async_music_search(music_query))
        if news_query:
            tasks.append(self._async_news_search(news_query))
        
        if tasks:
            results_list = await asyncio.gather(*tasks, return_exceptions=True)
            for key, value in results_list:
                results[key] = value
        
        return results
    
    async def _async_movie_search(self, query: str) -> Tuple[str, List]:
        """Async movie search"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.tmdb.search_movies,
            query
        )
        return 'movies', result
    
    async def _async_music_search(self, query: str) -> Tuple[str, List]:
        """Async music search"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.spotify.search_tracks,
            query
        )
        return 'music', result
    
    async def _async_news_search(self, query: str) -> Tuple[str, List]:
        """Async news search"""
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self.news.search_articles,
            query
        )
        return 'news', result


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def format_duration(ms: int) -> str:
    """Convert milliseconds to MM:SS format"""
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


def calculate_recommendation_score(item: Dict, user_preferences: Dict) -> float:
    """
    Calculate recommendation score based on item and user preferences
    
    Args:
        item: Item dictionary with attributes
        user_preferences: User preference dictionary
    
    Returns:
        Recommendation score (0-100)
    """
    score = 50  # Base score
    
    # Rating boost
    if 'rating' in item:
        score += (item['rating'] / 10) * 25
    
    # Popularity boost
    if 'popularity' in item:
        score += min(item['popularity'], 100) * 0.15
    
    return min(score, 100)


def deduplicate_recommendations(recommendations: List[Dict], 
                               key: str = 'id') -> List[Dict]:
    """Remove duplicate recommendations"""
    seen = set()
    unique = []
    
    for item in recommendations:
        if item.get(key) not in seen:
            seen.add(item.get(key))
            unique.append(item)
    
    return unique


# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

if __name__ == "__main__":
    # Example usage
    api_config = {
        'tmdb': 'your_tmdb_key',
        'spotify_id': 'your_spotify_id',
        'spotify_secret': 'your_spotify_secret',
        'news': 'your_news_api_key'
    }
    
    # Initialize clients
    tmdb = TMDbClient(api_config['tmdb'])
    spotify = SpotifyClient(api_config['spotify_id'], api_config['spotify_secret'])
    news = NewsAPIClient(api_config['news'])
    
    # Example: Search movies
    movies = tmdb.search_movies("Inception")
    print("Movies:", movies)
    
    # Example: Get trending movies
    trending = tmdb.get_trending_movies()
    print("Trending:", trending)
