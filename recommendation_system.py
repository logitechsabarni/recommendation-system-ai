import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import requests
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="PersonaAI - Recommendation Engine",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# PersonaAI Recommendation System\nAdvanced personalization powered by AI"
    }
)

# ============================================================================
# CUSTOM STYLING & THEMING
# ============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=DM+Serif+Display&display=swap');
    
    :root {
        --primary-color: #00D9FF;
        --secondary-color: #FF006E;
        --accent-color: #8338EC;
        --dark-bg: #0a0e27;
        --card-bg: #1a1f3a;
        --text-primary: #ffffff;
        --text-secondary: #b0b8d4;
        --success: #06FFA5;
        --warning: #FFB800;
    }
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
        color: var(--text-primary);
    }
    
    .main {
        padding: 2rem;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, rgba(0, 217, 255, 0.1) 0%, rgba(255, 0, 110, 0.1) 100%);
        border: 1px solid rgba(0, 217, 255, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.1);
    }
    
    .header-title {
        font-family: 'DM Serif Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00D9FF 0%, #FF006E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d2e47 100%);
        border: 1px solid rgba(0, 217, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(0, 217, 255, 0.5);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.15);
        transform: translateY(-4px);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00D9FF 0%, #8338EC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Product Card */
    .product-card {
        background: linear-gradient(135deg, #1a1f3a 0%, #22264a 100%);
        border: 1px solid rgba(0, 217, 255, 0.15);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .product-card:hover {
        border-color: #00D9FF;
        box-shadow: 0 12px 40px rgba(0, 217, 255, 0.2);
        transform: translateY(-8px);
    }
    
    .product-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
    }
    
    .product-category {
        display: inline-block;
        background: rgba(0, 217, 255, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.3);
        color: #00D9FF;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .product-score {
        background: linear-gradient(135deg, #00D9FF 0%, #8338EC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #00D9FF 0%, #8338EC 100%);
        color: #000;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(0, 217, 255, 0.3);
    }
    
    /* Slider Styling */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #00D9FF 0%, #8338EC 100%);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        background-color: rgba(0, 217, 255, 0.1);
        border: 1px solid rgba(0, 217, 255, 0.2);
        padding: 1rem 2rem;
        color: var(--text-secondary);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 217, 255, 0.2);
        border-color: #00D9FF;
        color: #00D9FF;
    }
    
    /* Sidebar */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #1a1f3a 0%, #16213e 100%);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        background-color: #16213e !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        color: var(--text-primary) !important;
        border-radius: 10px !important;
    }
    
    /* Success Messages */
    .stSuccess {
        background-color: rgba(6, 255, 165, 0.1) !important;
        border: 1px solid #06FFA5 !important;
        border-radius: 10px !important;
    }
    
    /* Info Messages */
    .stInfo {
        background-color: rgba(0, 217, 255, 0.1) !important;
        border: 1px solid #00D9FF !important;
        border-radius: 10px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(0, 217, 255, 0.1) !important;
        border: 1px solid rgba(0, 217, 255, 0.2) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# RECOMMENDATION SYSTEM CLASSES
# ============================================================================

class RecommendationEngine:
    """Advanced recommendation engine with multiple algorithms"""
    
    def __init__(self):
        self.users_df = None
        self.items_df = None
        self.interactions_df = None
        self.similarity_matrix = None
        
    def generate_sample_data(self):
        """Generate realistic sample data"""
        np.random.seed(42)
        
        # Movies/Products database
        items = {
            'item_id': range(1, 51),
            'title': self._generate_titles(),
            'category': np.random.choice(['Action', 'Drama', 'Comedy', 'Sci-Fi', 'Thriller'], 50),
            'genre': np.random.choice(['Adventure', 'Mystery', 'Romance', 'Horror', 'Animation'], 50),
            'rating': np.random.uniform(6.5, 9.5, 50),
            'release_year': np.random.randint(2018, 2024, 50),
            'popularity': np.random.uniform(0.1, 1.0, 50),
        }
        self.items_df = pd.DataFrame(items)
        
        # User profiles
        users = {
            'user_id': range(1, 101),
            'username': [f'User_{i}' for i in range(1, 101)],
            'join_date': [datetime.now() - timedelta(days=np.random.randint(1, 730)) for _ in range(100)],
            'preference_action': np.random.uniform(0, 1, 100),
            'preference_drama': np.random.uniform(0, 1, 100),
            'preference_comedy': np.random.uniform(0, 1, 100),
        }
        self.users_df = pd.DataFrame(users)
        
        # User-Item interactions
        interactions = []
        for user_id in range(1, 101):
            num_interactions = np.random.randint(5, 25)
            item_ids = np.random.choice(range(1, 51), num_interactions, replace=False)
            
            for item_id in item_ids:
                interactions.append({
                    'user_id': user_id,
                    'item_id': item_id,
                    'rating': np.random.uniform(3, 10),
                    'interaction_count': np.random.randint(1, 10),
                    'timestamp': datetime.now() - timedelta(days=np.random.randint(1, 365))
                })
        
        self.interactions_df = pd.DataFrame(interactions)
        
    def _generate_titles(self):
        """Generate realistic product/movie titles"""
        first_words = ['The', 'Beyond', 'Lost', 'Rise', 'Fall', 'Silent', 'Eternal', 'Quantum', 'Digital', 'Cosmic']
        second_words = ['Shadow', 'Dawn', 'Horizon', 'Realm', 'Code', 'Mind', 'City', 'World', 'Dream', 'Fire']
        third_words = ['Chronicles', 'Saga', 'Legacy', 'Rise', 'Protocol', 'Era', 'Quest', 'Path', 'Gateway', 'Prophecy']
        
        titles = []
        for _ in range(50):
            title = f"{np.random.choice(first_words)} {np.random.choice(second_words)} {np.random.choice(third_words)}"
            titles.append(title)
        return titles
    
    def collaborative_filtering(self, user_id: int, n_recommendations: int = 10) -> pd.DataFrame:
        """User-based collaborative filtering"""
        # Create user-item matrix
        user_item_matrix = self.interactions_df.pivot_table(
            index='user_id',
            columns='item_id',
            values='rating',
            fill_value=0
        )
        
        # Calculate similarity between users
        user_similarities = cosine_similarity(user_item_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarities,
            index=user_item_matrix.index,
            columns=user_item_matrix.index
        )
        
        # Find similar users
        similar_users = user_similarity_df[user_id].sort_values(ascending=False)[1:11]
        
        # Get items rated by similar users but not by current user
        user_rated = set(self.interactions_df[self.interactions_df['user_id'] == user_id]['item_id'])
        
        recommendations = {}
        for sim_user, similarity_score in similar_users.items():
            sim_user_items = self.interactions_df[self.interactions_df['user_id'] == sim_user]
            for _, row in sim_user_items.iterrows():
                if row['item_id'] not in user_rated:
                    if row['item_id'] not in recommendations:
                        recommendations[row['item_id']] = 0
                    recommendations[row['item_id']] += row['rating'] * similarity_score
        
        # Sort and get top recommendations
        top_items = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        rec_df = self.items_df[self.items_df['item_id'].isin([item[0] for item in top_items])].copy()
        rec_df['score'] = rec_df['item_id'].map(dict(top_items))
        rec_df['score'] = (rec_df['score'] / rec_df['score'].max() * 100).round(2)
        rec_df = rec_df.sort_values('score', ascending=False)
        
        return rec_df
    
    def content_based_filtering(self, user_id: int, n_recommendations: int = 10) -> pd.DataFrame:
        """Content-based filtering using item features"""
        user_interactions = self.interactions_df[self.interactions_df['user_id'] == user_id]
        
        if len(user_interactions) == 0:
            return pd.DataFrame()
        
        liked_items = user_interactions['item_id'].values
        liked_items_df = self.items_df[self.items_df['item_id'].isin(liked_items)]
        
        # Calculate average preference profile
        user_profile = {
            'avg_rating': liked_items_df['rating'].mean(),
            'avg_popularity': liked_items_df['popularity'].mean(),
            'avg_year': liked_items_df['release_year'].mean(),
        }
        
        # Find similar items
        unrated_items = self.items_df[~self.items_df['item_id'].isin(liked_items)]
        
        similarities = []
        for _, item in unrated_items.iterrows():
            rating_diff = abs(item['rating'] - user_profile['avg_rating']) / 10
            pop_diff = abs(item['popularity'] - user_profile['avg_popularity'])
            year_diff = abs(item['release_year'] - user_profile['avg_year']) / 10
            
            similarity = 1 - (rating_diff + pop_diff + year_diff) / 3
            similarities.append(similarity)
        
        unrated_items['similarity_score'] = similarities
        recommendations = unrated_items.nlargest(n_recommendations, 'similarity_score').copy()
        recommendations['score'] = (recommendations['similarity_score'] * 100).round(2)
        
        return recommendations[['item_id', 'title', 'category', 'genre', 'rating', 'score']]
    
    def hybrid_recommendation(self, user_id: int, n_recommendations: int = 10, 
                            collab_weight: float = 0.6, content_weight: float = 0.4) -> pd.DataFrame:
        """Hybrid approach combining collaborative and content-based filtering"""
        collab_recs = self.collaborative_filtering(user_id, n_recommendations * 2)
        content_recs = self.content_based_filtering(user_id, n_recommendations * 2)
        
        # Normalize scores
        if len(collab_recs) > 0:
            collab_recs['collab_score'] = collab_recs['score'] / collab_recs['score'].max()
        else:
            collab_recs['collab_score'] = 0
            
        if len(content_recs) > 0:
            content_recs['content_score'] = content_recs['score'] / content_recs['score'].max()
        else:
            content_recs['content_score'] = 0
        
        # Merge recommendations
        all_items = set(collab_recs['item_id']) | set(content_recs['item_id'])
        
        hybrid_scores = {}
        for item_id in all_items:
            collab_score = collab_recs[collab_recs['item_id'] == item_id]['score'].values
            content_score = content_recs[content_recs['item_id'] == item_id]['score'].values
            
            collab_score = collab_score[0] if len(collab_score) > 0 else 0
            content_score = content_score[0] if len(content_score) > 0 else 0
            
            hybrid_scores[item_id] = (collab_score * collab_weight + content_score * content_weight)
        
        sorted_items = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
        
        final_recs = self.items_df[self.items_df['item_id'].isin([item[0] for item in sorted_items])].copy()
        final_recs['score'] = final_recs['item_id'].map(dict(sorted_items))
        final_recs = final_recs.sort_values('score', ascending=False)
        
        return final_recs
    
    def trending_items(self, n_items: int = 10) -> pd.DataFrame:
        """Get trending items based on recent interactions"""
        recent_interactions = self.interactions_df[
            self.interactions_df['timestamp'] > datetime.now() - timedelta(days=30)
        ]
        
        trending = recent_interactions.groupby('item_id').agg({
            'interaction_count': 'sum',
            'rating': 'mean'
        }).reset_index()
        
        trending = trending.merge(self.items_df, on='item_id')
        trending['trend_score'] = (trending['interaction_count'] * trending['rating'] / 10)
        trending = trending.nlargest(n_items, 'trend_score')
        trending['score'] = (trending['trend_score'] / trending['trend_score'].max() * 100).round(2)
        
        return trending[['item_id', 'title', 'category', 'genre', 'rating', 'score']]

    def explain_recommendation(self, user_id: int, item_id: int, algo: str = "Hybrid") -> Dict:
        """Generate a human-readable explanation for why an item was recommended"""
        item = self.items_df[self.items_df['item_id'] == item_id]
        if item.empty:
            return {"reason": "Recommended for you", "confidence": 0.5, "tags": []}

        item = item.iloc[0]
        user_interactions = self.interactions_df[self.interactions_df['user_id'] == user_id]
        user_items = self.items_df[self.items_df['item_id'].isin(user_interactions['item_id'])]

        tags = []
        reason_parts = []

        # Category match
        if len(user_items) > 0:
            fav_category = user_interactions.merge(self.items_df, on='item_id')['category'].mode()
            if len(fav_category) > 0 and fav_category.iloc[0] == item['category']:
                reason_parts.append(f"matches your top category ({item['category']})")
                tags.append(f"🎯 {item['category']} fan")

        # Highly rated
        if item['rating'] >= 8.5:
            reason_parts.append("it's critically acclaimed")
            tags.append("⭐ Top Rated")

        # Trending
        recent = self.interactions_df[
            self.interactions_df['timestamp'] > datetime.now() - timedelta(days=14)
        ]
        if item_id in recent['item_id'].values:
            reason_parts.append("it's trending right now")
            tags.append("🔥 Trending")

        # Similar users
        if algo in ("Collaborative Filtering", "Hybrid"):
            reason_parts.append("users with similar taste loved it")
            tags.append("👥 Crowd Favourite")

        # Popularity
        if item['popularity'] > 0.7:
            tags.append("📈 Popular")

        if not reason_parts:
            reason_parts.append("it aligns with your viewing history")

        confidence = min(0.95, 0.55 + 0.1 * len(tags))
        reason = "Because " + " and ".join(reason_parts[:2])

        return {
            "reason": reason,
            "confidence": round(confidence, 2),
            "tags": tags[:3]
        }

    def apply_feedback(self, user_id: int, item_id: int, feedback: str):
        """Apply like/dislike feedback to update user interactions"""
        weight_map = {"like": 9.0, "dislike": 2.0, "neutral": 5.0}
        rating = weight_map.get(feedback, 5.0)

        existing = self.interactions_df[
            (self.interactions_df['user_id'] == user_id) &
            (self.interactions_df['item_id'] == item_id)
        ]

        if len(existing) > 0:
            self.interactions_df.loc[existing.index, 'rating'] = rating
        else:
            new_row = pd.DataFrame([{
                'user_id': user_id,
                'item_id': item_id,
                'rating': rating,
                'interaction_count': 1,
                'timestamp': datetime.now()
            }])
            self.interactions_df = pd.concat([self.interactions_df, new_row], ignore_index=True)

    # Mood → category/genre mapping
    MOOD_MAP = {
        "😄 Happy":    {"categories": ["Comedy", "Action"],    "genres": ["Animation", "Adventure"], "min_rating": 7.5},
        "😢 Sad":      {"categories": ["Drama"],               "genres": ["Romance", "Mystery"],      "min_rating": 7.0},
        "😴 Chill":    {"categories": ["Drama", "Comedy"],     "genres": ["Romance", "Adventure"],    "min_rating": 7.0},
        "😤 Pumped":   {"categories": ["Action", "Thriller"],  "genres": ["Adventure", "Horror"],     "min_rating": 7.0},
        "🤔 Curious":  {"categories": ["Sci-Fi", "Thriller"],  "genres": ["Mystery", "Horror"],       "min_rating": 7.5},
        "😱 Thrilled": {"categories": ["Thriller", "Sci-Fi"],  "genres": ["Horror", "Mystery"],       "min_rating": 7.0},
    }

    def mood_based_recommendation(self, user_id: int, mood: str, n_recommendations: int = 8) -> pd.DataFrame:
        """Return recommendations filtered and boosted by the user's current mood"""
        mood_prefs = self.MOOD_MAP.get(mood, {})
        base = self.hybrid_recommendation(user_id, n_recommendations * 3)

        if mood_prefs:
            cats = mood_prefs["categories"]
            genres = mood_prefs["genres"]
            min_r = mood_prefs["min_rating"]

            # Priority tier: matches category AND genre AND rating
            tier1 = base[
                base['category'].isin(cats) &
                base['genre'].isin(genres) &
                (base['rating'] >= min_r)
            ]
            # Second tier: matches category or genre
            tier2 = base[
                (base['category'].isin(cats) | base['genre'].isin(genres)) &
                ~base['item_id'].isin(tier1['item_id'])
            ]
            # Fill rest with remaining
            tier3 = base[~base['item_id'].isin(pd.concat([tier1, tier2])['item_id'])]
            result = pd.concat([tier1, tier2, tier3]).head(n_recommendations)
        else:
            result = base.head(n_recommendations)

        return result.reset_index(drop=True)

    def discover_new(self, user_id: int, n_recommendations: int = 8) -> pd.DataFrame:
        """Inject novelty — items outside user's usual categories, ranked by quality"""
        user_interactions = self.interactions_df[self.interactions_df['user_id'] == user_id]
        user_cats = self.items_df[
            self.items_df['item_id'].isin(user_interactions['item_id'])
        ]['category'].unique()

        # Prefer items from categories the user has NOT explored
        new_cats = self.items_df[~self.items_df['category'].isin(user_cats)]
        rated_ids = set(user_interactions['item_id'])
        unrated = new_cats[~new_cats['item_id'].isin(rated_ids)]

        if len(unrated) < n_recommendations:
            # Top-rated unseen items as fallback
            fallback = self.items_df[~self.items_df['item_id'].isin(rated_ids)]
            unrated = pd.concat([unrated, fallback]).drop_duplicates('item_id')

        result = unrated.sort_values('rating', ascending=False).head(n_recommendations).copy()
        result['score'] = (result['rating'] / 10 * 100).round(2)
        return result[['item_id', 'title', 'category', 'genre', 'rating', 'score']]

    # Time-of-day → preference mapping
    TIME_CONTEXT = {
        "morning":   {"boost_cats": ["Comedy", "Action"],           "label": "☀️ Morning",  "tip": "Energising picks to start your day"},
        "afternoon": {"boost_cats": ["Sci-Fi", "Action", "Thriller"],"label": "🌤️ Afternoon","tip": "Peak focus — great for complex stories"},
        "evening":   {"boost_cats": ["Drama", "Thriller"],          "label": "🌆 Evening",  "tip": "Wind-down with engaging dramas"},
        "night":     {"boost_cats": ["Drama", "Comedy"],            "label": "🌙 Night",    "tip": "Chill picks for late-night viewing"},
    }

    @staticmethod
    def get_time_of_day() -> str:
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"

    def context_aware_recommendation(self, user_id: int, n_recommendations: int = 8) -> pd.DataFrame:
        """Hybrid recs boosted by time-of-day context"""
        tod = self.get_time_of_day()
        boost_cats = self.TIME_CONTEXT[tod]["boost_cats"]
        base = self.hybrid_recommendation(user_id, n_recommendations * 3)

        boosted = base[base['category'].isin(boost_cats)]
        rest = base[~base['category'].isin(boost_cats)]
        result = pd.concat([boosted, rest]).head(n_recommendations)
        return result.reset_index(drop=True)

    def get_weekly_summary(self, user_id: int) -> Dict:
        """Stats summary for the past 7 days"""
        cutoff = datetime.now() - timedelta(days=7)
        week_ints = self.interactions_df[
            (self.interactions_df['user_id'] == user_id) &
            (self.interactions_df['timestamp'] >= cutoff)
        ]
        total_ints = self.interactions_df[self.interactions_df['user_id'] == user_id]

        if len(week_ints) == 0:
            top_cat = "—"
            avg_r = 0.0
            items_this_week = 0
        else:
            merged = week_ints.merge(self.items_df[['item_id','category']], on='item_id', how='left')
            top_cat = merged['category'].mode().iloc[0] if len(merged) > 0 else "—"
            avg_r = week_ints['rating'].mean()
            items_this_week = len(week_ints)

        return {
            "items_this_week": items_this_week,
            "avg_rating_this_week": round(avg_r, 1),
            "top_category_this_week": top_cat,
            "total_items_ever": len(total_ints),
            "streak_days": min(items_this_week, 7),
        }

    def get_user_badges(self, user_id: int) -> List[Dict]:
        """Calculate gamification badges earned by the user"""
        badges = []
        user_interactions = self.interactions_df[self.interactions_df['user_id'] == user_id]
        n_items = len(user_interactions)
        user_cats = self.items_df[
            self.items_df['item_id'].isin(user_interactions['item_id'])
        ]['category'].nunique()
        avg_r = user_interactions['rating'].mean() if n_items > 0 else 0

        # Milestone badges
        if n_items >= 5:
            badges.append({"icon": "🌱", "name": "Getting Started",  "desc": f"Reviewed {n_items} items"})
        if n_items >= 15:
            badges.append({"icon": "🔥", "name": "Power User",       "desc": "15+ interactions logged"})
        if n_items >= 20:
            badges.append({"icon": "👑", "name": "Super Fan",        "desc": "20+ items reviewed"})

        # Explorer badge
        if user_cats >= 3:
            badges.append({"icon": "🧭", "name": "Explorer",         "desc": f"Tried {user_cats} categories"})
        if user_cats >= 5:
            badges.append({"icon": "🌍", "name": "Genre Globetrotter","desc": "5+ genres explored"})

        # Quality taste badge
        if avg_r >= 7.5 and n_items >= 5:
            badges.append({"icon": "🎩", "name": "Connoisseur",      "desc": "Consistently high ratings"})

        # Trend catcher
        recent = self.interactions_df[
            self.interactions_df['timestamp'] > datetime.now() - timedelta(days=7)
        ]
        user_recent = recent[recent['user_id'] == user_id]
        if len(user_recent) >= 2:
            badges.append({"icon": "⚡", "name": "Trend Catcher",    "desc": "Active this week"})

        # Feedback badges (from session state — passed in)
        return badges


class PersonalizationAnalyzer:
    """Analyze user behavior and preferences"""
    
    def __init__(self, engine: RecommendationEngine):
        self.engine = engine
    
    def get_user_profile(self, user_id: int) -> Dict:
        """Generate detailed user profile"""
        user_interactions = self.engine.interactions_df[self.engine.interactions_df['user_id'] == user_id]
        
        if len(user_interactions) == 0:
            return {}
        
        interacted_items = self.engine.items_df[
            self.engine.items_df['item_id'].isin(user_interactions['item_id'])
        ]
        
        profile = {
            'total_interactions': len(user_interactions),
            'avg_rating': user_interactions['rating'].mean(),
            'favorite_category': interacted_items['category'].mode()[0] if len(interacted_items) > 0 else 'N/A',
            'favorite_genre': interacted_items['genre'].mode()[0] if len(interacted_items) > 0 else 'N/A',
            'avg_item_rating': interacted_items['rating'].mean() if len(interacted_items) > 0 else 0,
            'activity_level': 'High' if len(user_interactions) > 15 else 'Medium' if len(user_interactions) > 8 else 'Low',
            'items_reviewed': len(user_interactions),
        }
        
        return profile
    
    def get_category_preferences(self, user_id: int) -> pd.DataFrame:
        """Get user's preference distribution across categories"""
        user_interactions = self.engine.interactions_df[self.engine.interactions_df['user_id'] == user_id]
        interacted_items = self.engine.items_df[
            self.engine.items_df['item_id'].isin(user_interactions['item_id'])
        ]
        
        preferences = interacted_items['category'].value_counts().reset_index()
        preferences.columns = ['category', 'count']
        preferences['percentage'] = (preferences['count'] / preferences['count'].sum() * 100).round(1)
        
        return preferences


# ============================================================================
# INITIALIZATION & STATE MANAGEMENT
# ============================================================================

@st.cache_resource
def init_recommendation_engine():
    """Initialize recommendation engine with sample data"""
    engine = RecommendationEngine()
    engine.generate_sample_data()
    return engine

def initialize_session_state():
    """Initialize session state variables"""
    if 'engine' not in st.session_state:
        st.session_state.engine = init_recommendation_engine()
    
    if 'selected_user' not in st.session_state:
        st.session_state.selected_user = 1
    
    if 'selected_algo' not in st.session_state:
        st.session_state.selected_algo = 'Hybrid'
    
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    if 'recommendation_history' not in st.session_state:
        st.session_state.recommendation_history = []

    if 'feedback' not in st.session_state:
        # {item_id: "like" | "dislike" | "neutral"}
        st.session_state.feedback = {}

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'selected_mood' not in st.session_state:
        st.session_state.selected_mood = None

    if 'badges_seen' not in st.session_state:
        st.session_state.badges_seen = set()

    if 'items_per_page' not in st.session_state:
        st.session_state.items_per_page = 10

    if 'last_recommendations' not in st.session_state:
        st.session_state.last_recommendations = {}

initialize_session_state()

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_stats_visualizations(engine: RecommendationEngine):
    """Create summary statistics visualizations"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Total Items</div>
            <div class="metric-value">50</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Active Users</div>
            <div class="metric-value">100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Total Interactions</div>
            <div class="metric-value">""" + str(len(engine.interactions_df)) + """</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_rating = engine.items_df['rating'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Rating</div>
            <div class="metric-value">{avg_rating:.1f}★</div>
        </div>
        """, unsafe_allow_html=True)

def plot_category_distribution(engine: RecommendationEngine):
    """Plot category distribution"""
    category_counts = engine.items_df['category'].value_counts()
    
    fig = go.Figure(data=[
        go.Bar(
            x=category_counts.index,
            y=category_counts.values,
            marker=dict(
                color=category_counts.values,
                colorscale='Viridis',
                line=dict(color='rgba(0, 217, 255, 0.5)', width=2)
            ),
            text=category_counts.values,
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='<b>Items by Category</b>',
        xaxis_title='Category',
        yaxis_title='Count',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        hovermode='x unified',
        showlegend=False,
    )
    
    return fig

def plot_rating_distribution(engine: RecommendationEngine):
    """Plot rating distribution"""
    fig = px.histogram(
        engine.items_df,
        x='rating',
        nbins=15,
        title='<b>Rating Distribution</b>',
        color_discrete_sequence=['#00D9FF'],
    )
    
    fig.update_traces(
        marker=dict(line=dict(color='rgba(0, 217, 255, 0.5)', width=2)),
        hovertemplate='<b>Rating Range: %{x}</b><br>Count: %{y}<extra></extra>'
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        showlegend=False,
        xaxis_title='Rating',
        yaxis_title='Frequency'
    )
    
    return fig

def plot_user_preferences(analyzer: PersonalizationAnalyzer, user_id: int):
    """Plot user's category preferences"""
    preferences = analyzer.get_category_preferences(user_id)
    
    if len(preferences) == 0:
        st.info("No preference data available for this user.")
        return
    
    fig = go.Figure(data=[
        go.Pie(
            labels=preferences['category'],
            values=preferences['count'],
            hole=.3,
            marker=dict(
                line=dict(color='#0a0e27', width=2),
                colors=['#00D9FF', '#FF006E', '#8338EC', '#06FFA5', '#FFB800']
            ),
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>Items: %{value}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='<b>Category Preferences</b>',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        showlegend=True,
    )
    
    return fig

def plot_recommendations_comparison(recs_dict: Dict[str, pd.DataFrame]):
    """Compare recommendations from different algorithms"""
    items_appeared = {}
    
    for algo, recs in recs_dict.items():
        for _, row in recs.head(10).iterrows():
            item_id = row['item_id']
            if item_id not in items_appeared:
                items_appeared[item_id] = {}
            items_appeared[item_id][algo] = row['score']
    
    # Take top 8 items
    top_items = sorted(
        items_appeared.items(),
        key=lambda x: max(x[1].values()),
        reverse=True
    )[:8]
    
    trace_data = {}
    for item_id, algo_scores in top_items:
        for algo in recs_dict.keys():
            if algo not in trace_data:
                trace_data[algo] = []
            trace_data[algo].append(algo_scores.get(algo, 0))
    
    fig = go.Figure()
    colors = ['#00D9FF', '#FF006E', '#8338EC']
    
    for i, (algo, scores) in enumerate(trace_data.items()):
        fig.add_trace(go.Bar(
            x=[f"Item {iid}" for iid, _ in top_items],
            y=scores,
            name=algo,
            marker_color=colors[i % len(colors)],
            hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<extra></extra>'
        ))
    
    fig.update_layout(
        title='<b>Algorithm Comparison</b>',
        xaxis_title='Items',
        yaxis_title='Recommendation Score',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        hovermode='x unified'
    )
    
    return fig

def render_recommendation_cards(recommendations: pd.DataFrame, algo_name: str):
    """Render recommendation cards with explainability and feedback"""
    if len(recommendations) == 0:
        st.warning(f"No recommendations available from {algo_name} algorithm.")
        return

    st.subheader(f"🎯 {algo_name} Recommendations")
    engine = st.session_state.engine
    user_id = st.session_state.selected_user

    for idx, (_, rec) in enumerate(recommendations.head(10).iterrows(), 1):
        explanation = engine.explain_recommendation(user_id, rec['item_id'], algo_name)
        current_feedback = st.session_state.feedback.get(rec['item_id'], None)

        col1, col2, col3 = st.columns([4, 1, 1])

        with col1:
            tags_html = " ".join(
                f'<span style="background:rgba(131,56,236,0.2);border:1px solid rgba(131,56,236,0.5);'
                f'color:#b97bff;border-radius:20px;padding:2px 10px;font-size:0.75rem;">{t}</span>'
                for t in explanation["tags"]
            )
            conf_pct = int(explanation["confidence"] * 100)
            feedback_color = "#06FFA5" if current_feedback == "like" else ("#FF006E" if current_feedback == "dislike" else "#b0b8d4")
            feedback_label = {"like": "👍 Liked", "dislike": "👎 Disliked"}.get(current_feedback, "")
            st.markdown(f"""
            <div class="product-card">
                <div class="product-title">#{idx} • {rec['title']}</div>
                <div style="display:flex;gap:0.5rem;margin-bottom:0.6rem;flex-wrap:wrap;">
                    <span class="product-category">{rec['category']}</span>
                    <span class="product-category">{rec['genre']}</span>
                    {tags_html}
                </div>
                <div style="color:#b0b8d4;font-size:0.9rem;margin-bottom:0.6rem;">
                    Rating: <span style="color:#FFB800;">{'★' * int(rec['rating'] / 2)}</span> {rec['rating']:.1f}
                </div>
                <div style="background:rgba(0,217,255,0.07);border-left:3px solid #00D9FF;padding:0.5rem 0.8rem;border-radius:0 8px 8px 0;font-size:0.85rem;color:#b0d4ff;">
                    💡 <em>{explanation['reason']}</em>
                    <span style="float:right;color:#00D9FF;font-weight:600;">{conf_pct}% match</span>
                </div>
                {'<div style="margin-top:0.4rem;font-size:0.8rem;color:' + feedback_color + ';">' + feedback_label + '</div>' if feedback_label else ''}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            score = rec['score']
            st.markdown(f"""
            <div style="text-align:center;padding:1rem;">
                <div style="font-size:2rem;font-weight:700;background:linear-gradient(135deg,#00D9FF 0%,#8338EC 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
                    {score:.0f}%
                </div>
                <div style="color:#b0b8d4;font-size:0.8rem;margin-top:0.5rem;">Score</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.write("")
            like_btn = st.button("👍", key=f"like_{algo_name}_{rec['item_id']}", help="Like this")
            dislike_btn = st.button("👎", key=f"dislike_{algo_name}_{rec['item_id']}", help="Not for me")
            fav_btn = st.button("❤️", key=f"fav_{algo_name}_{rec['item_id']}", help="Favourite")

            if like_btn:
                st.session_state.feedback[rec['item_id']] = "like"
                engine.apply_feedback(user_id, rec['item_id'], "like")
                st.rerun()
            if dislike_btn:
                st.session_state.feedback[rec['item_id']] = "dislike"
                engine.apply_feedback(user_id, rec['item_id'], "dislike")
                st.rerun()
            if fav_btn:
                if rec['item_id'] not in st.session_state.favorites:
                    st.session_state.favorites.append(rec['item_id'])
                    st.success("Added to favourites!")


def render_badges(badges: List[Dict]):
    """Render gamification badge cards in a horizontal grid"""
    if not badges:
        st.info("No badges yet — start rating items to earn your first badge! 🌱")
        return

    cols = st.columns(min(len(badges), 4))
    for i, badge in enumerate(badges):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1f3a,#2a1f4a);border:1px solid rgba(131,56,236,0.4);
                border-radius:14px;padding:1rem;text-align:center;margin-bottom:0.5rem;">
                <div style="font-size:2rem;">{badge['icon']}</div>
                <div style="font-weight:700;color:#b97bff;font-size:0.9rem;margin:0.3rem 0;">{badge['name']}</div>
                <div style="color:#8090b0;font-size:0.75rem;">{badge['desc']}</div>
            </div>
            """, unsafe_allow_html=True)


def plot_user_similarity_heatmap(engine: RecommendationEngine, n_users: int = 15) -> go.Figure:
    """Cosine-similarity heatmap for a sample of users"""
    user_item_matrix = engine.interactions_df.pivot_table(
        index='user_id', columns='item_id', values='rating', fill_value=0
    )
    sample_ids = user_item_matrix.index[:n_users]
    matrix_sample = user_item_matrix.loc[sample_ids]
    sim = cosine_similarity(matrix_sample)

    fig = go.Figure(data=go.Heatmap(
        z=sim,
        x=[f"U{i}" for i in sample_ids],
        y=[f"U{i}" for i in sample_ids],
        colorscale='Plasma',
        hovertemplate='User %{x} ↔ User %{y}<br>Similarity: %{z:.2f}<extra></extra>',
        showscale=True,
    ))
    fig.update_layout(
        title='<b>User Similarity Heatmap</b>',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        xaxis_title='User', yaxis_title='User',
    )
    return fig


def plot_interaction_timeline(engine: RecommendationEngine, user_id: int) -> go.Figure:
    """Daily interaction activity timeline for a specific user"""
    user_ints = engine.interactions_df[engine.interactions_df['user_id'] == user_id].copy()
    user_ints['date'] = pd.to_datetime(user_ints['timestamp']).dt.date
    daily = user_ints.groupby('date').agg(interactions=('item_id', 'count'), avg_rating=('rating', 'mean')).reset_index()
    daily = daily.sort_values('date')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily['date'], y=daily['interactions'],
        name='Interactions', marker_color='rgba(0,217,255,0.6)',
        hovertemplate='%{x}<br>Interactions: %{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=daily['date'], y=daily['avg_rating'],
        name='Avg Rating', yaxis='y2',
        line=dict(color='#FF006E', width=2),
        mode='lines+markers',
        hovertemplate='%{x}<br>Avg Rating: %{y:.1f}<extra></extra>'
    ))
    fig.update_layout(
        title='<b>Activity Timeline</b>',
        xaxis_title='Date',
        yaxis=dict(title='Interactions', gridcolor='rgba(255,255,255,0.05)'),
        yaxis2=dict(title='Avg Rating', overlaying='y', side='right', range=[0, 10]),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        legend=dict(orientation='h', y=1.1),
        barmode='overlay'
    )
    return fig


def plot_popularity_vs_rating(engine: RecommendationEngine) -> go.Figure:
    """Bubble chart: popularity vs rating, sized by interaction count"""
    interaction_counts = engine.interactions_df.groupby('item_id').size().reset_index(name='n_interactions')
    df = engine.items_df.merge(interaction_counts, on='item_id', how='left').fillna({'n_interactions': 1})

    color_map = {'Action': '#00D9FF', 'Drama': '#FF006E', 'Comedy': '#06FFA5',
                 'Sci-Fi': '#8338EC', 'Thriller': '#FFB800'}

    fig = go.Figure()
    for cat in df['category'].unique():
        sub = df[df['category'] == cat]
        fig.add_trace(go.Scatter(
            x=sub['popularity'], y=sub['rating'],
            mode='markers',
            name=cat,
            marker=dict(
                size=sub['n_interactions'] * 3 + 6,
                color=color_map.get(cat, '#ffffff'),
                opacity=0.75,
                line=dict(color='white', width=0.5)
            ),
            text=sub['title'],
            hovertemplate='<b>%{text}</b><br>Popularity: %{x:.2f}<br>Rating: %{y:.1f}<extra></extra>'
        ))
    fig.update_layout(
        title='<b>Popularity vs Rating (bubble = interactions)</b>',
        xaxis_title='Popularity Score',
        yaxis_title='Rating',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        legend=dict(orientation='h', y=-0.15)
    )
    return fig


def plot_user_activity_heatmap(engine: RecommendationEngine) -> go.Figure:
    """Users × Categories interaction heatmap"""
    merged = engine.interactions_df.merge(engine.items_df[['item_id', 'category']], on='item_id')
    hmap = merged.groupby(['user_id', 'category'])['rating'].mean().unstack(fill_value=0)
    sample = hmap.iloc[:20]  # top 20 users for readability

    fig = go.Figure(data=go.Heatmap(
        z=sample.values,
        x=sample.columns.tolist(),
        y=[f"U{i}" for i in sample.index],
        colorscale='Viridis',
        hovertemplate='User %{y} · %{x}<br>Avg Rating: %{z:.1f}<extra></extra>',
        showscale=True,
    ))
    fig.update_layout(
        title='<b>Users × Category Avg Rating</b>',
        xaxis_title='Category', yaxis_title='User',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
    )
    return fig


def plot_score_distribution_by_algo(engine: RecommendationEngine, user_id: int) -> go.Figure:
    """Box plot of recommendation scores for each algorithm"""
    algo_scores = {}
    for aname, afn in [
        ("Collaborative", lambda: engine.collaborative_filtering(user_id, 20)),
        ("Content-Based",  lambda: engine.content_based_filtering(user_id, 20)),
        ("Hybrid",         lambda: engine.hybrid_recommendation(user_id, 20)),
        ("Trending",       lambda: engine.trending_items(20)),
    ]:
        try:
            recs = afn()
            if len(recs) > 0:
                algo_scores[aname] = recs['score'].tolist()
        except Exception:
            pass

    colors = ['#00D9FF', '#FF006E', '#8338EC', '#FFB800']
    fig = go.Figure()
    for i, (algo, scores) in enumerate(algo_scores.items()):
        fig.add_trace(go.Box(
            y=scores, name=algo,
            marker_color=colors[i % len(colors)],
            boxmean='sd',
            hovertemplate=f'<b>{algo}</b><br>Score: %{{y:.1f}}<extra></extra>'
        ))
    fig.update_layout(
        title='<b>Score Distribution by Algorithm</b>',
        yaxis_title='Recommendation Score',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        showlegend=False
    )
    return fig


def plot_top_items_leaderboard(engine: RecommendationEngine, n: int = 10) -> go.Figure:
    """Horizontal ranked bar — top items by weighted score"""
    counts = engine.interactions_df.groupby('item_id').agg(
        n=('interaction_count', 'sum'), avg_r=('rating', 'mean')
    ).reset_index()
    counts['score'] = (counts['n'] * counts['avg_r']).round(2)
    top = counts.nlargest(n, 'score').merge(engine.items_df[['item_id', 'title', 'category']], on='item_id')
    top = top.sort_values('score')

    color_map = {'Action': '#00D9FF', 'Drama': '#FF006E', 'Comedy': '#06FFA5',
                 'Sci-Fi': '#8338EC', 'Thriller': '#FFB800'}
    colors = [color_map.get(c, '#b0b8d4') for c in top['category']]

    fig = go.Figure(go.Bar(
        x=top['score'], y=top['title'],
        orientation='h',
        marker_color=colors,
        text=[f"{v:.0f}" for v in top['score']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
    ))
    fig.update_layout(
        title='<b>🏆 Top Items Leaderboard</b>',
        xaxis_title='Weighted Score',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        margin=dict(l=160)
    )
    return fig


def plot_release_year_trend(engine: RecommendationEngine) -> go.Figure:
    """Items and avg rating by release year"""
    year_df = engine.items_df.groupby('release_year').agg(
        count=('item_id', 'count'), avg_rating=('rating', 'mean')
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=year_df['release_year'], y=year_df['count'],
        name='Items Released',
        marker_color='rgba(131,56,236,0.6)',
        hovertemplate='Year: %{x}<br>Items: %{y}<extra></extra>'
    ))
    fig.add_trace(go.Scatter(
        x=year_df['release_year'], y=year_df['avg_rating'],
        name='Avg Rating', yaxis='y2',
        line=dict(color='#FFB800', width=2),
        mode='lines+markers',
        hovertemplate='Year: %{x}<br>Avg Rating: %{y:.2f}<extra></extra>'
    ))
    fig.update_layout(
        title='<b>Items & Ratings by Release Year</b>',
        xaxis_title='Year',
        yaxis=dict(title='Item Count', gridcolor='rgba(255,255,255,0.05)'),
        yaxis2=dict(title='Avg Rating', overlaying='y', side='right', range=[5, 10]),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        legend=dict(orientation='h', y=1.1)
    )
    return fig


def plot_mood_radar(engine: RecommendationEngine) -> go.Figure:
    """Radar chart showing item coverage across mood-relevant categories"""
    mood_labels = list(engine.MOOD_MAP.keys())
    cat_counts = engine.items_df['category'].value_counts()

    # For each mood, sum items across its categories
    coverage = []
    for mood, prefs in engine.MOOD_MAP.items():
        total = sum(cat_counts.get(c, 0) for c in prefs['categories'])
        coverage.append(total)

    # Close the radar loop
    coverage_closed = coverage + [coverage[0]]
    labels_closed = mood_labels + [mood_labels[0]]

    fig = go.Figure(go.Scatterpolar(
        r=coverage_closed,
        theta=labels_closed,
        fill='toself',
        fillcolor='rgba(0,217,255,0.15)',
        line=dict(color='#00D9FF', width=2),
        hovertemplate='Mood: %{theta}<br>Item Coverage: %{r}<extra></extra>'
    ))
    fig.update_layout(
        title='<b>Mood Coverage Radar</b>',
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, gridcolor='rgba(255,255,255,0.1)', color='#b0b8d4'),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='#b0b8d4')
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        showlegend=False
    )
    return fig


def plot_confidence_gauge(engine: RecommendationEngine, user_id: int) -> go.Figure:
    """Gauge chart: average recommendation confidence for selected user"""
    recs = engine.hybrid_recommendation(user_id, 10)
    if len(recs) == 0:
        avg_conf = 0.5
    else:
        confs = [engine.explain_recommendation(user_id, iid)['confidence'] for iid in recs['item_id']]
        avg_conf = sum(confs) / len(confs)

    pct = round(avg_conf * 100)
    color = '#06FFA5' if pct >= 75 else '#FFB800' if pct >= 55 else '#FF006E'

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=pct,
        delta={'reference': 70, 'increasing': {'color': '#06FFA5'}, 'decreasing': {'color': '#FF006E'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#b0b8d4'},
            'bar': {'color': color},
            'bgcolor': 'rgba(26,31,58,0.8)',
            'bordercolor': 'rgba(255,255,255,0.1)',
            'steps': [
                {'range': [0, 50],  'color': 'rgba(255,0,110,0.15)'},
                {'range': [50, 75], 'color': 'rgba(255,184,0,0.15)'},
                {'range': [75, 100],'color': 'rgba(6,255,165,0.15)'},
            ],
            'threshold': {'line': {'color': 'white', 'width': 2}, 'value': 70}
        },
        number={'suffix': '%', 'font': {'color': color}},
        title={'text': f"<b>Avg Match Confidence — User {user_id}</b>", 'font': {'color': '#b0b8d4'}}
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
        height=280
    )
    return fig


def plot_genre_distribution(engine: RecommendationEngine) -> go.Figure:
    """Sunburst: Category → Genre breakdown"""
    fig = px.sunburst(
        engine.items_df,
        path=['category', 'genre'],
        color='rating',
        color_continuous_scale='plasma',
        title='<b>Category → Genre Breakdown</b>',
        hover_data={'rating': ':.1f'}
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Space Grotesk'),
    )
    return fig


def plot_feedback_summary(feedback: dict, engine) -> go.Figure:
    """Bar chart of liked vs disliked items by category"""
    if not feedback:
        return go.Figure()

    rows = []
    for item_id, fb in feedback.items():
        item = engine.items_df[engine.items_df['item_id'] == item_id]
        if not item.empty:
            rows.append({"category": item.iloc[0]['category'], "feedback": fb})

    if not rows:
        return go.Figure()

    df = pd.DataFrame(rows)
    summary = df.groupby(['category', 'feedback']).size().reset_index(name='count')

    fig = px.bar(
        summary, x='category', y='count', color='feedback',
        color_discrete_map={"like": "#06FFA5", "dislike": "#FF006E"},
        barmode='group',
        title="Your Feedback by Category",
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#b0b8d4',
        legend_title_text='Feedback'
    )
    return fig


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">✨ PersonaAI</div>
        <div class="header-subtitle">Intelligent Recommendation Engine - Powered by Advanced ML</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎯 Recommendations",
        "📊 Analytics",
        "👤 User Profile",
        "🔬 Algorithm Details",
        "⚙️ Settings",
        "💬 Chat",
        "❤️ Favourites"
    ])
    
    engine = st.session_state.engine
    analyzer = PersonalizationAnalyzer(engine)

    # ========================================================================
    # SIDEBAR — Live User Snapshot
    # ========================================================================
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:1rem 0 0.5rem;">
            <div style="font-size:2.5rem;">✨</div>
            <div style="font-weight:700;font-size:1.1rem;color:#00D9FF;">PersonaAI</div>
            <div style="color:#b0b8d4;font-size:0.75rem;">Recommendation Engine</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Time-of-day context badge
        tod = engine.get_time_of_day()
        tod_info = engine.TIME_CONTEXT[tod]
        st.markdown(f"""
        <div style="background:rgba(0,217,255,0.08);border:1px solid rgba(0,217,255,0.25);
            border-radius:10px;padding:0.7rem 1rem;margin-bottom:0.8rem;text-align:center;">
            <div style="font-size:1.1rem;font-weight:700;color:#00D9FF;">{tod_info['label']}</div>
            <div style="color:#b0b8d4;font-size:0.78rem;margin-top:0.2rem;">{tod_info['tip']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Current user quick stats
        uid = st.session_state.selected_user
        profile = analyzer.get_user_profile(uid)
        weekly = engine.get_weekly_summary(uid)
        badges = engine.get_user_badges(uid)

        if profile:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#1a1f3a,#2a1f4a);border:1px solid rgba(131,56,236,0.3);
                border-radius:12px;padding:1rem;margin-bottom:0.8rem;">
                <div style="font-weight:700;color:#b97bff;margin-bottom:0.6rem;">👤 User {uid}</div>
                <div style="color:#b0b8d4;font-size:0.82rem;line-height:1.9;">
                    📂 <b>{profile.get('items_reviewed', 0)}</b> items reviewed<br>
                    ⭐ Avg rating: <b>{profile.get('avg_rating', 0):.1f}</b><br>
                    🎯 Fav: <b>{profile.get('favorite_category','—')}</b><br>
                    🏆 <b>{len(badges)}</b> badge{'s' if len(badges) != 1 else ''} earned
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Weekly summary
        st.markdown("**📅 This Week**")
        wc1, wc2 = st.columns(2)
        wc1.metric("Items", weekly['items_this_week'])
        wc2.metric("Avg ★", weekly['avg_rating_this_week'] if weekly['avg_rating_this_week'] > 0 else "—")
        if weekly['streak_days'] > 0:
            st.caption(f"🔥 {weekly['streak_days']}-day activity streak  ·  Top: **{weekly['top_category_this_week']}**")

        st.divider()

        # Favourites count
        fav_count = len(st.session_state.favorites)
        fb_count = len(st.session_state.feedback)
        st.markdown(f"""
        <div style="color:#b0b8d4;font-size:0.82rem;line-height:2;">
            ❤️ <b>{fav_count}</b> saved favourite{'s' if fav_count != 1 else ''}<br>
            👍 <b>{fb_count}</b> item{'s' if fb_count != 1 else ''} rated<br>
            💬 <b>{len(st.session_state.chat_history) // 2}</b> chat exchange{'s' if len(st.session_state.chat_history) // 2 != 1 else ''}
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Quick context-aware button
        if st.button("⚡ Context Recs (Now)", use_container_width=True,
                     help=f"Recommendations tuned for {tod_info['label']}"):
            st.session_state.show_context_recs = True
            st.session_state.show_recs = False
            st.session_state.show_discover = False
    
    # ========================================================================
    # TAB 1: RECOMMENDATIONS
    # ========================================================================
    with tab1:
        # --- Badge toast notifications ---
        badges = engine.get_user_badges(st.session_state.selected_user)
        new_badges = [b for b in badges if b['name'] not in st.session_state.badges_seen]
        for b in new_badges:
            st.toast(f"{b['icon']} New badge: **{b['name']}** — {b['desc']}", icon=b['icon'])
            st.session_state.badges_seen.add(b['name'])

        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.subheader("Configure Recommendations")

            # User selection
            selected_user = st.selectbox(
                "Select User",
                options=engine.users_df['user_id'].values,
                format_func=lambda x: f"User {x}",
                key="user_selector"
            )
            st.session_state.selected_user = selected_user

            st.divider()

            # --- MOOD SELECTOR ---
            st.write("**🎭 How are you feeling?**")
            mood_options = ["— Skip —"] + list(engine.MOOD_MAP.keys())
            selected_mood = st.selectbox(
                "Mood",
                mood_options,
                label_visibility="collapsed",
                key="mood_selector"
            )
            st.session_state.selected_mood = None if selected_mood == "— Skip —" else selected_mood

            st.divider()

            # Algorithm selection
            st.write("**Select Algorithm**")
            algo_options = ["Collaborative Filtering", "Content-Based", "Hybrid", "Trending"]
            selected_algos = st.multiselect(
                "Choose one or more algorithms:",
                algo_options,
                default=["Hybrid"],
                label_visibility="collapsed"
            )

            st.divider()

            # Number of recommendations
            n_recs = st.slider(
                "Number of Recommendations",
                min_value=3,
                max_value=20,
                value=10,
                step=1
            )

            # Advanced settings
            with st.expander("⚙️ Advanced Settings"):
                collab_weight = st.slider(
                    "Collaborative Weight (Hybrid)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.6,
                    step=0.1
                )
                content_weight = 1.0 - collab_weight

                freshness_weight = st.slider(
                    "Content Freshness Weight",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.3,
                    step=0.1
                )

            gen_col, disc_col = st.columns(2)
            with gen_col:
                if st.button("🚀 Generate", use_container_width=True):
                    st.session_state.show_recs = True
                    st.session_state.show_discover = False
                    st.session_state.show_context_recs = False
            with disc_col:
                if st.button("🎲 Discover New", use_container_width=True, help="Step outside your comfort zone"):
                    st.session_state.show_discover = True
                    st.session_state.show_recs = False
                    st.session_state.show_context_recs = False

        with col2:
            # --- CONTEXT-AWARE path (triggered from sidebar) ---
            if st.session_state.get('show_context_recs', False):
                tod = engine.get_time_of_day()
                tod_info = engine.TIME_CONTEXT[tod]
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(0,217,255,0.08),rgba(131,56,236,0.08));
                    border:1px solid rgba(0,217,255,0.3);border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
                    <b style="color:#00D9FF;">{tod_info['label']} — Context-Aware Picks</b>
                    <p style="color:#b0b8d4;font-size:0.9rem;margin:0.3rem 0 0;">{tod_info['tip']}</p>
                </div>
                """, unsafe_allow_html=True)
                ctx_recs = engine.context_aware_recommendation(selected_user, n_recs)
                render_recommendation_cards(ctx_recs, f"Context ({tod_info['label']})")
                # Store for export
                st.session_state.last_recommendations[f"Context ({tod_info['label']})"] = ctx_recs

            # --- DISCOVER NEW path ---
            elif st.session_state.get('show_discover', False):
                st.markdown("""
                <div style="background:linear-gradient(135deg,rgba(6,255,165,0.08),rgba(131,56,236,0.08));
                    border:1px solid rgba(6,255,165,0.3);border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
                    <b style="color:#06FFA5;">🎲 Discover Something New</b>
                    <p style="color:#b0b8d4;font-size:0.9rem;margin:0.3rem 0 0;">
                    These picks are <em>outside</em> your usual taste — you might be surprised!
                    </p>
                </div>
                """, unsafe_allow_html=True)
                discover_recs = engine.discover_new(selected_user, n_recs)
                render_recommendation_cards(discover_recs, "Discover New")
                st.session_state.last_recommendations["Discover New"] = discover_recs

            # --- MOOD path ---
            elif st.session_state.selected_mood and st.session_state.get('show_recs', False):
                mood = st.session_state.selected_mood
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,rgba(255,184,0,0.08),rgba(255,0,110,0.08));
                    border:1px solid rgba(255,184,0,0.3);border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
                    <b style="color:#FFB800;">🎭 Mood Mode: {mood}</b>
                    <p style="color:#b0b8d4;font-size:0.9rem;margin:0.3rem 0 0;">
                    Recommendations tuned to match how you're feeling right now.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                mood_recs = engine.mood_based_recommendation(selected_user, mood, n_recs)
                render_recommendation_cards(mood_recs, f"Mood: {mood}")
                st.session_state.last_recommendations[f"Mood: {mood}"] = mood_recs

            # --- NORMAL path ---
            elif st.session_state.get('show_recs', False):
                recommendations_dict = {}

                for algo in selected_algos:
                    with st.spinner(f"Generating {algo} recommendations..."):
                        if algo == "Collaborative Filtering":
                            recommendations_dict[algo] = engine.collaborative_filtering(
                                selected_user, n_recs
                            )
                        elif algo == "Content-Based":
                            recommendations_dict[algo] = engine.content_based_filtering(
                                selected_user, n_recs
                            )
                        elif algo == "Hybrid":
                            recommendations_dict[algo] = engine.hybrid_recommendation(
                                selected_user, n_recs, collab_weight
                            )
                        elif algo == "Trending":
                            recommendations_dict[algo] = engine.trending_items(n_recs)

                # Store for export
                st.session_state.last_recommendations = recommendations_dict

                for algo, recs in recommendations_dict.items():
                    render_recommendation_cards(recs, algo)
                    st.divider()

                if len(recommendations_dict) > 1:
                    st.subheader("📈 Algorithm Comparison")
                    comparison_fig = plot_recommendations_comparison(recommendations_dict)
                    st.plotly_chart(comparison_fig, use_container_width=True, key="tab1_algo_comparison")

                st.session_state.recommendation_history.append({
                    'timestamp': datetime.now(),
                    'user_id': selected_user,
                    'algorithms': selected_algos,
                    'count': n_recs
                })
            else:
                st.info("👈 Select options and click 'Generate' — or try **🎲 Discover New** for surprises!")
    
    # ========================================================================
    # TAB 2: ANALYTICS
    # ========================================================================
    with tab2:
        st.subheader("System Analytics & Insights")

        # Statistics
        create_stats_visualizations(engine)

        st.divider()

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.plotly_chart(plot_category_distribution(engine), use_container_width=True, key="tab2_category_dist")

        with col2:
            st.plotly_chart(plot_rating_distribution(engine), use_container_width=True, key="tab2_rating_dist")

        # User interaction heatmap
        st.subheader("User Interaction Insights")
        col1, col2, col3 = st.columns(3)

        with col1:
            most_rated_item = engine.interactions_df.groupby('item_id')['interaction_count'].sum().idxmax()
            most_rated_title = engine.items_df[engine.items_df['item_id'] == most_rated_item]['title'].values[0]
            st.metric("Most Popular Item", most_rated_title, "👑")

        with col2:
            avg_interactions = engine.interactions_df.groupby('user_id').size().mean()
            st.metric("Avg Items Per User", f"{avg_interactions:.1f}", "📊")

        with col3:
            highly_rated = len(engine.items_df[engine.items_df['rating'] >= 8.5])
            st.metric("Premium Items (8.5+★)", highly_rated, "⭐")

        st.divider()

        # --- Feedback Summary ---
        st.subheader("👍👎 Your Feedback Summary")
        feedback = st.session_state.feedback
        if feedback:
            likes = sum(1 for v in feedback.values() if v == "like")
            dislikes = sum(1 for v in feedback.values() if v == "dislike")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Rated", len(feedback))
            col2.metric("👍 Liked", likes)
            col3.metric("👎 Disliked", dislikes)
            fb_fig = plot_feedback_summary(feedback, engine)
            if fb_fig.data:
                st.plotly_chart(fb_fig, use_container_width=True, key="tab2_feedback_summary")
        else:
            st.info("Rate some recommendations (👍 / 👎) to see your feedback analytics here.")

        st.divider()

        # --- A/B Algorithm Comparison ---
        st.subheader("🔬 A/B Algorithm Comparison")
        st.caption("Compare average recommendation scores across all algorithms for the selected user")
        ab_user = st.session_state.selected_user
        ab_data = {}
        for aname, afn in [
            ("Collaborative", lambda: engine.collaborative_filtering(ab_user, 10)),
            ("Content-Based",  lambda: engine.content_based_filtering(ab_user, 10)),
            ("Hybrid",         lambda: engine.hybrid_recommendation(ab_user, 10)),
            ("Trending",       lambda: engine.trending_items(10)),
        ]:
            try:
                recs = afn()
                ab_data[aname] = recs['score'].mean() if len(recs) > 0 else 0
            except Exception:
                ab_data[aname] = 0

        ab_fig = go.Figure(go.Bar(
            x=list(ab_data.keys()),
            y=list(ab_data.values()),
            marker=dict(
                color=list(ab_data.values()),
                colorscale="Viridis",
                showscale=False
            ),
            text=[f"{v:.1f}%" for v in ab_data.values()],
            textposition='outside'
        ))
        ab_fig.update_layout(
            title="Average Match Score by Algorithm",
            yaxis_title="Avg Score (%)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#b0b8d4',
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(ab_fig, use_container_width=True, key="tab2_ab_comparison")
        best_algo = max(ab_data, key=ab_data.get)
        st.success(f"🏆 Best performing algorithm for User {ab_user}: **{best_algo}** ({ab_data[best_algo]:.1f}% avg score)")

        st.divider()

        # --- Popularity vs Rating Bubble ---
        st.subheader("🫧 Popularity vs Rating")
        st.plotly_chart(plot_popularity_vs_rating(engine), use_container_width=True, key="tab2_popularity_rating")

        st.divider()

        # --- User Activity Heatmap ---
        st.subheader("🗺️ User × Category Engagement Map")
        st.plotly_chart(plot_user_activity_heatmap(engine), use_container_width=True, key="tab2_user_activity")

        st.divider()

        # --- Top Items Leaderboard ---
        st.subheader("🏆 Top Items Leaderboard")
        st.plotly_chart(plot_top_items_leaderboard(engine), use_container_width=True, key="tab2_leaderboard")

        st.divider()

        # --- Release Year Trend ---
        st.subheader("📅 Release Year Trends")
        st.plotly_chart(plot_release_year_trend(engine), use_container_width=True, key="tab2_release_year")

        st.divider()

        # --- User Similarity Heatmap ---
        st.subheader("🤝 User Similarity Heatmap")
        st.caption("Cosine similarity between the first 15 users based on their rating patterns")
        st.plotly_chart(plot_user_similarity_heatmap(engine), use_container_width=True, key="tab2_user_similarity")

        st.divider()

        # --- Category → Genre Sunburst ---
        st.subheader("🌐 Category → Genre Breakdown")
        st.plotly_chart(plot_genre_distribution(engine), use_container_width=True, key="tab2_genre_sunburst")
    
    # ========================================================================
    # TAB 3: USER PROFILE
    # ========================================================================
    with tab3:
        st.subheader("User Profile & Behavior Analysis")
        
        selected_profile_user = st.selectbox(
            "Select User to Analyze",
            options=engine.users_df['user_id'].values,
            format_func=lambda x: f"User {x}",
            key="profile_user_selector"
        )
        
        profile = analyzer.get_user_profile(selected_profile_user)
        
        if profile:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Items Reviewed</div>
                    <div class="metric-value">{profile['items_reviewed']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Avg Rating</div>
                    <div class="metric-value">{profile['avg_rating']:.1f}★</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Favorite Category</div>
                    <div class="metric-value">{profile['favorite_category']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Activity Level</div>
                    <div class="metric-value">{profile['activity_level']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.plotly_chart(
                    plot_user_preferences(analyzer, selected_profile_user),
                    use_container_width=True,
                    key="tab3_user_preferences"
                )
            
            with col2:
                st.write("**User Summary**")
                user_data = engine.users_df[engine.users_df['user_id'] == selected_profile_user].iloc[0]
                st.write(f"**Username:** {user_data['username']}")
                st.write(f"**Member Since:** {user_data['join_date'].strftime('%B %d, %Y')}")
                st.write(f"**Favorite Genre:** {profile['favorite_genre']}")
                st.write(f"**Engagement:** {profile['activity_level']}")
                
                # Show user's rated items
                st.subheader("Recently Reviewed Items")
                user_interactions = engine.interactions_df[
                    engine.interactions_df['user_id'] == selected_profile_user
                ].sort_values('timestamp', ascending=False).head(5)
                
                if len(user_interactions) > 0:
                    for _, interaction in user_interactions.iterrows():
                        item = engine.items_df[engine.items_df['item_id'] == interaction['item_id']].iloc[0]
                        st.write(f"• **{item['title']}** - Rating: {'★' * int(interaction['rating'] / 2)} {interaction['rating']:.1f}")
                else:
                    st.info("No reviewed items yet")
        else:
            st.warning("No profile data available for this user.")

        # --- Gamification Badges ---
        st.divider()
        st.subheader("🏆 Badges & Achievements")
        badges = engine.get_user_badges(selected_profile_user)
        render_badges(badges)
        if badges:
            st.caption(f"You've earned **{len(badges)}** badge{'s' if len(badges) != 1 else ''}. Keep exploring to unlock more!")

        st.divider()

        # --- Confidence Gauge ---
        st.subheader("🎯 Match Confidence Gauge")
        st.caption("How confidently the hybrid algorithm recommends for this user")
        st.plotly_chart(plot_confidence_gauge(engine, selected_profile_user), use_container_width=True, key="tab3_confidence_gauge")

        st.divider()

        # --- Activity Timeline ---
        st.subheader("📅 Activity Timeline")
        st.plotly_chart(plot_interaction_timeline(engine, selected_profile_user), use_container_width=True, key="tab3_activity_timeline")

        st.divider()

        # --- Score Distribution ---
        st.subheader("📦 Algorithm Score Distribution")
        st.caption("Box plot showing the spread of recommendation scores per algorithm")
        st.plotly_chart(plot_score_distribution_by_algo(engine, selected_profile_user), use_container_width=True, key="tab3_score_distribution")
    
    # ========================================================================
    # TAB 4: ALGORITHM DETAILS
    # ========================================================================
    with tab4:
        st.subheader("Recommendation Algorithms Explained")
        
        col1, col2 = st.columns([1, 2], gap="large")
        
        with col1:
            algo_selected = st.radio(
                "Algorithm",
                ["Collaborative Filtering", "Content-Based", "Hybrid", "Trending"]
            )
        
        with col2:
            if algo_selected == "Collaborative Filtering":
                st.write("### Collaborative Filtering")
                st.write("""
                **How it works:**
                - Finds users with similar rating patterns
                - Recommends items liked by similar users
                - Based on the "wisdom of crowds" principle
                
                **Advantages:**
                - ✅ Discovers new items in the same taste community
                - ✅ No need for detailed item descriptions
                - ✅ Learns from implicit feedback
                
                **Disadvantages:**
                - ❌ Cold start problem (new users/items)
                - ❌ Sparse data issues
                - ❌ Popular items tend to dominate
                
                **Best for:** Items with rich interaction history
                """)
                
                with st.expander("📊 Mathematical Details"):
                    st.write("""
                    ```
                    User Similarity = Cosine Similarity(User A ratings, User B ratings)
                    
                    Recommendation Score = Σ(Similar Users' Ratings × Similarity Score)
                    ```
                    """)
            
            elif algo_selected == "Content-Based":
                st.write("### Content-Based Filtering")
                st.write("""
                **How it works:**
                - Analyzes features of items users liked
                - Finds similar items with matching characteristics
                - Uses item metadata for recommendations
                
                **Advantages:**
                - ✅ Works well for new items (no history needed)
                - ✅ Can explain recommendations
                - ✅ No cold start for items
                
                **Disadvantages:**
                - ❌ Requires good item descriptions
                - ❌ Limited discovery (stays in same category)
                - ❌ Difficult for subjective preferences
                
                **Best for:** Items with rich metadata
                """)
                
                with st.expander("📊 Mathematical Details"):
                    st.write("""
                    ```
                    Item Similarity = Distance(Item A features, Item B features)
                    
                    User Profile = Average(Features of liked items)
                    
                    Recommendation Score = Σ(Item Similarity × User Interest)
                    ```
                    """)
            
            elif algo_selected == "Hybrid":
                st.write("### Hybrid Approach")
                st.write("""
                **How it works:**
                - Combines Collaborative & Content-Based methods
                - Takes best of both approaches
                - Weights each algorithm's contribution
                
                **Advantages:**
                - ✅ Mitigates cold start problems
                - ✅ Balances serendipity and relevance
                - ✅ More robust recommendations
                - ✅ Adaptable to different scenarios
                
                **Disadvantages:**
                - ❌ More complex implementation
                - ❌ Higher computational cost
                - ❌ Requires tuning weights
                
                **Best for:** Production recommenders
                """)
                
                with st.expander("📊 Mathematical Details"):
                    st.write("""
                    ```
                    Hybrid Score = (α × Collab Score) + (β × Content Score)
                    
                    where α + β = 1 (normalized weights)
                    
                    α typically ranges from 0.4 to 0.7
                    ```
                    """)
            
            elif algo_selected == "Trending":
                st.write("### Trending & Popularity")
                st.write("""
                **How it works:**
                - Ranks items by recent popularity
                - Measures interaction velocity & ratings
                - Time-weighted scoring
                
                **Advantages:**
                - ✅ Fresh, timely recommendations
                - ✅ Great for discovery features
                - ✅ Easy to implement
                - ✅ Reduces diversity of very old content
                
                **Disadvantages:**
                - ❌ Not personalized
                - ❌ Bias toward mainstream items
                - ❌ Misses niche interests
                
                **Best for:** Explore/Discover pages
                """)
                
                with st.expander("📊 Mathematical Details"):
                    st.write("""
                    ```
                    Trend Score = (Interaction Count × Avg Rating) / Time Decay
                    
                    Time Decay = e^(-λ × days_since_interaction)
                    ```
                    """)

        st.divider()

        # --- Mood Radar ---
        st.subheader("🎭 Mood Coverage Radar")
        st.caption("How many items the catalog can serve for each mood profile")
        col1, col2 = st.columns([1, 1], gap="large")
        with col1:
            st.plotly_chart(plot_mood_radar(engine), use_container_width=True, key="tab4_mood_radar")
        with col2:
            st.markdown("""
            <div style="padding:1rem;color:#b0b8d4;font-size:0.9rem;line-height:1.8;">
            <b style="color:#00D9FF;">How to read this:</b><br>
            Each axis represents a mood. The further the point extends from the center,
            the more items the catalog can serve for that mood state.<br><br>
            A well-balanced radar means the system can personalise recommendations
            equally well regardless of the user's current feeling.
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # --- Algorithm Score Distribution ---
        st.subheader("📦 Algorithm Score Spread")
        st.caption("Compare score distributions across all algorithms for the current user")
        st.plotly_chart(
            plot_score_distribution_by_algo(engine, st.session_state.selected_user),
            use_container_width=True,
            key="tab4_score_distribution"
        )

    # ========================================================================
    # TAB 5: SETTINGS
    # ========================================================================
    with tab5:
        st.subheader("System Settings & Configuration")
        
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.write("### Display Preferences")
            items_per_page = st.slider(
                "Items per page",
                min_value=5,
                max_value=20,
                value=10
            )
            
            theme = st.selectbox(
                "Theme",
                ["Dark Mode", "Light Mode"]
            )
            
            language = st.selectbox(
                "Language",
                ["English", "Spanish", "French", "German"]
            )
        
        with col2:
            st.write("### Algorithm Configuration")
            enable_cf = st.checkbox("Enable Collaborative Filtering", value=True)
            enable_cb = st.checkbox("Enable Content-Based", value=True)
            enable_trending = st.checkbox("Enable Trending", value=True)
            
            min_sim_threshold = st.slider(
                "Minimum Similarity Threshold",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.05
            )
        
        st.divider()
        
        st.write("### Recommendation History")
        if st.session_state.recommendation_history:
            history_df = pd.DataFrame(st.session_state.recommendation_history)
            st.dataframe(
                history_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No recommendation history yet")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export Settings", use_container_width=True):
                settings = {
                    'items_per_page': items_per_page,
                    'theme': theme,
                    'language': language,
                    'min_sim_threshold': min_sim_threshold,
                }
                st.json(settings)
        
        with col2:
            if st.button("🔄 Reset to Defaults", use_container_width=True):
                st.success("Settings reset to defaults!")
        
        with col3:
            if st.button("💾 Save Settings", use_container_width=True):
                st.success("Settings saved successfully!")
    
    # ========================================================================
    # TAB 6: CHAT-BASED RECOMMENDATIONS
    # ========================================================================
    with tab6:
        st.subheader("💬 Chat with PersonaAI")
        st.caption("Ask me anything — 'Suggest underrated sci-fi movies', 'What's trending?', 'Find me something like Inception'")

        # Render chat history
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_input = st.chat_input("Ask for a recommendation...")

        if user_input:
            # Save user message
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            # Parse intent and generate recommendation
            query_lower = user_input.lower()
            engine_ref = st.session_state.engine
            uid = st.session_state.selected_user

            response_lines = []

            # Detect intent keywords
            wants_trending = any(k in query_lower for k in ["trend", "popular", "hot", "this week", "right now"])
            wants_genre = None
            for g in ["sci-fi", "action", "drama", "comedy", "thriller", "horror", "animation", "adventure", "mystery", "romance"]:
                if g in query_lower:
                    wants_genre = g.title()
                    break
            wants_new = any(k in query_lower for k in ["new", "discover", "fresh", "surprise", "underrated", "hidden"])
            wants_hybrid = any(k in query_lower for k in ["personali", "for me", "suggest", "recommend", "like me"])

            if wants_trending:
                recs = engine_ref.trending_items(5)
                response_lines.append("🔥 **Here are today's trending picks:**\n")
            elif wants_genre:
                recs = engine_ref.hybrid_recommendation(uid, 10)
                recs = recs[recs['genre'].str.lower() == wants_genre.lower()]
                if len(recs) == 0:
                    recs = engine_ref.hybrid_recommendation(uid, 10)
                recs = recs.head(5)
                response_lines.append(f"🎬 **Top {wants_genre} picks for you:**\n")
            elif wants_new:
                # Shuffle for novelty
                recs = engine_ref.hybrid_recommendation(uid, 20)
                recs = recs.sample(min(5, len(recs)), random_state=None)
                response_lines.append("✨ **Stepping outside your comfort zone — here's something fresh:**\n")
            else:
                recs = engine_ref.hybrid_recommendation(uid, 5)
                response_lines.append("🎯 **Personalised recommendations just for you:**\n")

            if len(recs) == 0:
                response_lines.append("Hmm, I couldn't find a match. Try asking differently!")
            else:
                for i, (_, r) in enumerate(recs.iterrows(), 1):
                    exp = engine_ref.explain_recommendation(uid, r['item_id'])
                    conf = int(exp["confidence"] * 100)
                    tags_str = "  ".join(exp["tags"])
                    response_lines.append(
                        f"**{i}. {r['title']}** `{r['category']} · {r['genre']}`  \n"
                        f"   ⭐ {r['rating']:.1f}  |  {conf}% match  |  {tags_str}  \n"
                        f"   💡 _{exp['reason']}_\n"
                    )

            response_text = "\n".join(response_lines)
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text)

    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #b0b8d4; padding: 2rem; font-size: 0.9rem;">
        <p>✨ <b>PersonaAI</b> - Advanced Recommendation Engine</p>
        <p>Built with Streamlit | Powered by ML & AI</p>
        <p style="margin-top: 1rem; font-size: 0.8rem;">
            © 2024 PersonaAI. All rights reserved. | 
            <a href="#" style="color: #00D9FF;">Privacy Policy</a> | 
            <a href="#" style="color: #00D9FF;">Terms of Service</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
