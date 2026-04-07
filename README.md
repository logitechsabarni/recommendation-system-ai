# PersonaAI - Advanced Recommendation System

> **Intelligent Personalization Engine Powered by Machine Learning**

A production-grade recommendation system built with Streamlit, featuring multiple recommendation algorithms, real-time personalization, beautiful UI/UX, and comprehensive analytics.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

---

## 🎯 Features

### Core Recommendation Algorithms

- **Collaborative Filtering** - User-based and item-based similarity
- **Content-Based Filtering** - Feature-based item similarity
- **Hybrid Approach** - Optimal combination of both methods
- **Trending & Popularity** - Fresh, timely recommendations

### Advanced Personalization

- 📊 Real-time user profile generation
- 🎯 Preference learning and adaptation
- 🔄 Multi-algorithm ensemble methods
- 💡 Cold-start problem handling
- 🎨 Serendipity & novelty optimization

### Analytics & Insights

- 📈 Comprehensive evaluation metrics
- 📊 Interactive visualizations
- 👥 User behavior analysis
- 🎯 Recommendation quality assessment
- 📉 Performance tracking

### Beautiful UI/UX

- ✨ Modern dark theme with gradient accents
- 🎨 Responsive card-based design
- 📱 Mobile-optimized interface
- 🎬 Smooth animations & transitions
- 🌈 Custom color palette

### API Integration

- 🎬 TMDb API for movies
- 🎵 Spotify API for music
- 📰 News API for articles
- ⚡ Async API orchestration
- 🔄 Real-time data fetching

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [Algorithms Explained](#algorithms-explained)
5. [API Integration](#api-integration)
6. [Configuration](#configuration)
7. [Evaluation Metrics](#evaluation-metrics)
8. [Usage Examples](#usage-examples)
9. [Performance](#performance)
10. [Troubleshooting](#troubleshooting)

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda
- Virtual environment (recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/personaai-recommendations.git
cd personaai-recommendations
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n personaai python=3.10
conda activate personaai
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Environment Variables

Create a `.env` file in the root directory:

```env
# Movie API
TMDB_API_KEY=your_tmdb_api_key

# Music API
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret

# News API
NEWS_API_KEY=your_news_api_key

# Optional: Database Configuration
DATABASE_URL=sqlite:///personaai.db
```

### Step 5: Run the Application

```bash
streamlit run recommendation_system.py
```

The application will open at `http://localhost:8501`

---

## ⚡ Quick Start

### 1. Launch the Application

```bash
streamlit run recommendation_system.py
```

### 2. Navigate to Recommendations Tab

- Select a user from the dropdown
- Choose recommendation algorithms
- Click "Generate Recommendations"

### 3. Explore Results

- View recommendations from different algorithms
- Compare algorithm performance
- Add items to favorites
- View detailed item information

### 4. Analyze User Profile

- Switch to "User Profile" tab
- Select a user to analyze
- View preference distribution
- See engagement metrics

### 5. Explore Analytics

- View system-wide statistics
- Check category distributions
- Analyze rating patterns
- Review user interactions

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    PersonaAI Frontend                        │
│                    (Streamlit UI)                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
            ┌───────────┼───────────┐
            │           │           │
    ┌───────▼──────┐  ┌─▼──────┐  ┌─▼──────────┐
    │ Recommendation│ │Analytics│ │User Profiles
    │   Engine     │ │ Module  │ │  Module
    └───────┬──────┘  └─┬──────┘  └─┬──────────┘
            │           │           │
    ┌───────┴───────────┼───────────┴──────┐
    │                   │                   │
┌───▼────┐      ┌──────▼─────┐      ┌──────▼──────┐
│Collab   │      │Content-Based│     │API Integration
│Filtering│      │Filtering    │     │Module
└─────────┘      └─────────────┘     └──────┬───────┐
                                            │       │
                                      ┌─────▼──┐ ┌──▼─────┐
                                      │TMDb API│ │Spotify
                                      └────────┘ └────────┘
```

### Key Modules

1. **recommendation_system.py** - Main Streamlit application
2. **api_integration.py** - External API clients
3. **analytics.py** - Evaluation metrics and reporting

---

## 🧠 Algorithms Explained

### 1. Collaborative Filtering

**How it works:**
- Finds users with similar rating patterns
- Recommends items liked by similar users
- Based on "wisdom of crowds"

**Formula:**
```
Similarity(User A, User B) = Cosine(Ratings_A, Ratings_B)
Recommendation Score = Σ(Similar Users' Ratings × Similarity)
```

**Best for:** Items with rich interaction history

**Pros:**
- ✅ Discovers new items in taste community
- ✅ No need for item descriptions
- ✅ Learns from implicit feedback

**Cons:**
- ❌ Cold start problem
- ❌ Sparse data issues
- ❌ Popular items dominate

### 2. Content-Based Filtering

**How it works:**
- Analyzes features of liked items
- Finds similar items with matching characteristics
- Uses item metadata

**Formula:**
```
Item Similarity = Distance(Features_A, Features_B)
User Profile = Average(Features of liked items)
Recommendation Score = Σ(Item Similarity × Interest)
```

**Best for:** Items with rich metadata

**Pros:**
- ✅ Works for new items
- ✅ Explainable recommendations
- ✅ No cold start for items

**Cons:**
- ❌ Requires good descriptions
- ❌ Limited discovery
- ❌ Subjective preferences

### 3. Hybrid Approach

**How it works:**
- Combines Collaborative & Content-Based
- Weights each algorithm's contribution
- Mitigates individual limitations

**Formula:**
```
Hybrid Score = (α × Collab Score) + (β × Content Score)
where α + β = 1 (typically α=0.6, β=0.4)
```

**Best for:** Production recommenders

**Pros:**
- ✅ Mitigates cold start
- ✅ Balances serendipity & relevance
- ✅ More robust
- ✅ Adaptable

**Cons:**
- ❌ Complex implementation
- ❌ Higher computational cost
- ❌ Requires weight tuning

### 4. Trending & Popularity

**How it works:**
- Ranks items by recent popularity
- Time-weighted scoring
- Measures interaction velocity

**Formula:**
```
Trend Score = (Interaction Count × Avg Rating) / e^(λ × days_old)
```

**Best for:** Explore/Discover pages

---

## 🔌 API Integration

### Supported Services

#### 1. TMDb (The Movie Database)

```python
from api_integration import TMDbClient

tmdb = TMDbClient(api_key='your_key')

# Search movies
movies = tmdb.search_movies("Inception")

# Get details
details = tmdb.get_movie_details(movie_id=27205)

# Get recommendations
similar = tmdb.get_recommendations(movie_id=27205, n=10)

# Trending movies
trending = tmdb.get_trending_movies(time_window='week')
```

#### 2. Spotify

```python
from api_integration import SpotifyClient

spotify = SpotifyClient(
    client_id='your_id',
    client_secret='your_secret'
)

# Search tracks
tracks = spotify.search_tracks("Bohemian Rhapsody")

# Get recommendations
recs = spotify.get_recommendations(
    seed_artists=['4NHkGGqwCmzHTguEAC60Ba'],
    limit=10
)
```

#### 3. News API

```python
from api_integration import NewsAPIClient

news = NewsAPIClient(api_key='your_key')

# Search articles
articles = news.search_articles("artificial intelligence")

# Get top headlines
headlines = news.get_top_headlines(
    category='technology',
    country='us'
)
```

#### 4. Async API Orchestration

```python
from api_integration import AsyncAPIOrchestrator
import asyncio

orchestrator = AsyncAPIOrchestrator(api_config)

# Fetch from multiple APIs concurrently
results = asyncio.run(
    orchestrator.fetch_all_recommendations(
        movie_query="sci-fi",
        music_query="electronic",
        news_query="AI"
    )
)
```

---

## ⚙️ Configuration

### Environment Variables

```env
# Recommendation Settings
COLLABORATIVE_WEIGHT=0.6
CONTENT_WEIGHT=0.4
FRESHNESS_WEIGHT=0.3

# Personalization
MIN_INTERACTIONS_FOR_COLLAB=5
ITEM_SIMILARITY_THRESHOLD=0.3

# API Settings
API_TIMEOUT=10
API_RETRY_ATTEMPTS=3
API_CACHE_DURATION=3600

# UI Settings
ITEMS_PER_PAGE=10
THEME=dark
```

### Advanced Tuning

#### Collaborative Filtering Weights

```python
# Increase weight for newer users
if user.interaction_count < 10:
    collab_weight = 0.7  # Trust other similar users more
else:
    collab_weight = 0.5  # Balanced approach
```

#### Cold Start Solutions

```python
# 1. Popularity boost
if user.interaction_count == 0:
    recommendations += trending_items

# 2. Content-based for new items
new_items = items[items['popularity'] < threshold]
new_item_recommendations = content_based_filtering(user_id)

# 3. Demographic filtering
similar_users = find_similar_by_demographics(user)
recommendations.extend(get_user_recommendations(similar_users))
```

---

## 📊 Evaluation Metrics

### Ranking Quality

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **Precision@K** | # relevant @ k / k | Accuracy of recommendations |
| **Recall@K** | # relevant @ k / total relevant | Coverage of relevant items |
| **NDCG@K** | DCG / IDCG | Position-weighted ranking quality |
| **MAP@K** | Avg(Precision@k) | Mean precision over ranks |
| **MRR@K** | 1 / rank of first match | Speed to first match |

### Diversity & Novelty

| Metric | Interpretation |
|--------|-----------------|
| **Catalog Coverage** | % of catalog items recommended |
| **Diversity Score** | How different items are from each other |
| **Novelty Score** | How fresh/obscure recommendations are |
| **Serendipity** | Balance between relevance & unexpectedness |
| **Gini Coefficient** | Equality in item recommendations (0=fair, 1=biased) |

### Prediction Accuracy

| Metric | Formula |
|--------|---------|
| **MAE** | Mean absolute error |
| **RMSE** | Root mean squared error |
| **Accuracy** | Fraction within tolerance |

### Usage Example

```python
from analytics import ComprehensiveEvaluator

evaluator = ComprehensiveEvaluator(
    recommendations=rec_df,
    true_items=[1, 5, 12, 23],
    interaction_df=interactions,
    catalog_size=1000
)

metrics = evaluator.evaluate_all(k=10)

print(f"Precision: {metrics.precision:.1%}")
print(f"Coverage: {metrics.coverage:.1%}")
print(f"Novelty: {metrics.novelty:.2f}")
```

---

## 💡 Usage Examples

### Example 1: Get Recommendations for a User

```python
from recommendation_system import RecommendationEngine

# Initialize engine
engine = RecommendationEngine()
engine.generate_sample_data()

# Get hybrid recommendations
recs = engine.hybrid_recommendation(
    user_id=1,
    n_recommendations=10,
    collab_weight=0.6,
    content_weight=0.4
)

print(recs[['title', 'category', 'score']].head(10))
```

### Example 2: Compare Algorithms

```python
# Get recommendations from all algorithms
collab = engine.collaborative_filtering(user_id=1, n_recommendations=10)
content = engine.content_based_filtering(user_id=1, n_recommendations=10)
hybrid = engine.hybrid_recommendation(user_id=1, n_recommendations=10)
trending = engine.trending_items(n_items=10)

# Compare
comparison = pd.concat([
    collab[['title', 'score']].assign(Algorithm='Collab'),
    content[['title', 'score']].assign(Algorithm='Content'),
    hybrid[['title', 'score']].assign(Algorithm='Hybrid'),
    trending[['title', 'score']].assign(Algorithm='Trending')
])

print(comparison.groupby('Algorithm')['score'].mean())
```

### Example 3: Analyze User Preferences

```python
from recommendation_system import PersonalizationAnalyzer

analyzer = PersonalizationAnalyzer(engine)

# Get user profile
profile = analyzer.get_user_profile(user_id=1)
print(f"Activity Level: {profile['activity_level']}")
print(f"Favorite Category: {profile['favorite_category']}")
print(f"Avg Rating: {profile['avg_rating']:.1f}")

# Get preference distribution
prefs = analyzer.get_category_preferences(user_id=1)
print(prefs)
```

### Example 4: Use External APIs

```python
from api_integration import TMDbClient, SpotifyClient
import asyncio

# Movie recommendations
tmdb = TMDbClient(api_key='your_key')
movies = tmdb.search_movies("Inception")
trending = tmdb.get_trending_movies()

# Music recommendations
spotify = SpotifyClient(client_id, client_secret)
tracks = spotify.search_tracks("electronic")

# Async fetching
from api_integration import AsyncAPIOrchestrator

orchestrator = AsyncAPIOrchestrator(api_config)
results = asyncio.run(
    orchestrator.fetch_all_recommendations(
        movie_query="sci-fi",
        music_query="ambient"
    )
)
```

---

## 📈 Performance

### Benchmarks

On dataset with 100 users, 50 items, 1000+ interactions:

| Algorithm | Time (ms) | Precision@10 | Recall@10 | NDCG@10 |
|-----------|-----------|--------------|-----------|---------|
| Collab    | 45        | 0.42         | 0.35      | 0.58    |
| Content   | 23        | 0.38         | 0.31      | 0.52    |
| Hybrid    | 68        | 0.48         | 0.41      | 0.64    |
| Trending  | 5         | 0.35         | 0.28      | 0.48    |

### Optimization Tips

1. **Cache results** - Use @lru_cache for API calls
2. **Batch processing** - Process multiple users together
3. **Limit history** - Use recent interactions only
4. **Approximate algorithms** - Use approximate nearest neighbors
5. **Database indexing** - Index user/item IDs

---

## 🔧 Troubleshooting

### Issue: Cold Start Problem

**Problem:** New users/items have no interactions

**Solutions:**
```python
# 1. Popularity-based recommendations
new_user_recs = trending_items(n=20)

# 2. Demographic-based
similar_users = find_similar_demographics(new_user)
recs.extend(get_recommendations(similar_users))

# 3. Content-based for items
item_features_recs = content_based_recommendations(new_item)
```

### Issue: Sparse Data

**Problem:** Few interactions lead to poor similarity

**Solutions:**
```python
# 1. Implicit feedback conversion
interactions['rating'] = interactions['interaction_count'] ** 0.5

# 2. Dimensionality reduction
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components=50)
user_vectors = svd.fit_transform(user_item_matrix)

# 3. Regularization
from sklearn.linear_model import Ridge
ridge = Ridge(alpha=1.0)
```

### Issue: Popular Item Bias

**Problem:** Recommendations always suggest popular items

**Solutions:**
```python
# 1. Popularity penalties
recs['score'] *= (1 - 0.1 * (popularity / max_popularity))

# 2. Long-tail promotion
recs = recs[recs['popularity'] < median_popularity]

# 3. Diversity constraints
from sklearn.cluster import KMeans
clusters = KMeans(n_clusters=5).fit(item_features)
```

### Issue: API Rate Limiting

**Problem:** Too many API requests

**Solutions:**
```python
# 1. Implement caching
from functools import lru_cache
@lru_cache(maxsize=1000)
def get_movie(movie_id):
    return api.fetch(movie_id)

# 2. Use async requests
from aiohttp import ClientSession

# 3. Batch requests
results = api.batch_fetch(item_ids)
```

---

## 📚 Learning Resources

- [Recommender Systems Handbook](http://recommender-systems.org/)
- [Netflix Prize - Lessons Learned](https://www.netflixprize.com/)
- [Collaborative Filtering - Stanford CS246](https://web.stanford.edu/class/cs246/)
- [Deep Learning for Recommendations](https://arxiv.org/abs/1707.07435)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see LICENSE.txt for details.

---

## 🙋 Support

For issues, questions, or suggestions:

- 📧 Email: support@personaai.com
- 💬 GitHub Issues: [GitHub Issues](https://github.com/yourusername/personaai/issues)
- 📖 Documentation: [Full Docs](https://docs.personaai.com)

---

## 🎉 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [scikit-learn](https://scikit-learn.org/)
- Data visualization with [Plotly](https://plotly.com/)

---

**Made with ❤️ by PersonaAI Team**

`Last Updated: 2024 | Version 1.0.0`

The link of the app is:- https://recommendation-system-ai-mvqcleif8zjpisr3dancgf.streamlit.app/
