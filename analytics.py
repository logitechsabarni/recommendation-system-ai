"""
Advanced Analytics & Evaluation Metrics
========================================
Comprehensive metrics for evaluating recommendation system performance
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, 
    precision_score, recall_score, f1_score
)
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# METRICS DATACLASSES
# ============================================================================

@dataclass
class RecommendationMetrics:
    """Container for recommendation metrics"""
    precision: float
    recall: float
    f1_score: float
    ndcg: float
    map_score: float
    rmse: float
    mae: float
    coverage: float
    diversity: float
    novelty: float
    serendipity: float


@dataclass
class UserEngagementMetrics:
    """Container for user engagement metrics"""
    ctr: float  # Click-through rate
    conversion_rate: float
    avg_rating: float
    repeat_rate: float
    time_to_click: float


# ============================================================================
# RANKING METRICS
# ============================================================================

class RankingMetrics:
    """Metrics for evaluating ranking quality"""
    
    @staticmethod
    def precision_at_k(true_items: List[int], predicted_items: List[int], k: int = 10) -> float:
        """
        Precision@K: Fraction of recommended items that are relevant
        
        Args:
            true_items: List of relevant item IDs
            predicted_items: List of predicted item IDs
            k: Number of top items to consider
        
        Returns:
            Precision@K score (0-1)
        """
        predicted_k = predicted_items[:k]
        hits = len(set(predicted_k) & set(true_items))
        return hits / k if k > 0 else 0
    
    @staticmethod
    def recall_at_k(true_items: List[int], predicted_items: List[int], k: int = 10) -> float:
        """
        Recall@K: Fraction of relevant items that are recommended
        
        Args:
            true_items: List of relevant item IDs
            predicted_items: List of predicted item IDs
            k: Number of top items to consider
        
        Returns:
            Recall@K score (0-1)
        """
        predicted_k = predicted_items[:k]
        hits = len(set(predicted_k) & set(true_items))
        return hits / len(true_items) if len(true_items) > 0 else 0
    
    @staticmethod
    def ndcg_at_k(true_items: List[int], predicted_items: List[int], k: int = 10) -> float:
        """
        Normalized Discounted Cumulative Gain@K
        Measures ranking quality considering position
        
        Args:
            true_items: List of relevant item IDs (in ideal order)
            predicted_items: List of predicted item IDs
            k: Number of top items to consider
        
        Returns:
            NDCG@K score (0-1)
        """
        # DCG calculation
        dcg = 0
        for i, item in enumerate(predicted_items[:k]):
            if item in true_items:
                dcg += 1 / np.log2(i + 2)  # position-based discount
        
        # IDCG calculation (ideal ranking)
        idcg = 0
        for i in range(min(k, len(true_items))):
            idcg += 1 / np.log2(i + 2)
        
        return dcg / idcg if idcg > 0 else 0
    
    @staticmethod
    def map_at_k(true_items: List[int], predicted_items: List[int], k: int = 10) -> float:
        """
        Mean Average Precision@K
        Measures ranking quality with position-based weighting
        
        Args:
            true_items: List of relevant item IDs
            predicted_items: List of predicted item IDs
            k: Number of top items to consider
        
        Returns:
            MAP@K score (0-1)
        """
        score = 0
        hits = 0
        
        for i, item in enumerate(predicted_items[:k]):
            if item in true_items:
                hits += 1
                score += hits / (i + 1)
        
        return score / len(true_items) if len(true_items) > 0 else 0
    
    @staticmethod
    def mrr_at_k(true_items: List[int], predicted_items: List[int], k: int = 10) -> float:
        """
        Mean Reciprocal Rank@K
        Measures how quickly first relevant item appears
        
        Args:
            true_items: List of relevant item IDs
            predicted_items: List of predicted item IDs
            k: Number of top items to consider
        
        Returns:
            MRR@K score (0-1)
        """
        for i, item in enumerate(predicted_items[:k]):
            if item in true_items:
                return 1 / (i + 1)
        return 0


# ============================================================================
# DIVERSITY & NOVELTY METRICS
# ============================================================================

class DiversityMetrics:
    """Metrics for measuring recommendation diversity"""
    
    @staticmethod
    def intra_list_diversity(recommendations: pd.DataFrame, 
                            feature_cols: List[str]) -> float:
        """
        Intra-list Diversity: How different items are from each other
        Uses cosine distance between item feature vectors
        
        Args:
            recommendations: DataFrame with recommended items
            feature_cols: List of feature column names
        
        Returns:
            Diversity score (0-1)
        """
        if len(recommendations) < 2:
            return 0
        
        from sklearn.metrics.pairwise import cosine_distances
        
        # Extract features
        features = recommendations[feature_cols].values
        
        # Calculate distances
        distances = cosine_distances(features)
        
        # Average distance
        n = len(distances)
        avg_distance = distances[np.triu_indices(n, k=1)].mean()
        
        return min(avg_distance, 1.0)
    
    @staticmethod
    def category_diversity(recommendations: pd.DataFrame, 
                          category_col: str = 'category') -> float:
        """
        Category Diversity: Fraction of unique categories in recommendations
        
        Args:
            recommendations: DataFrame with recommended items
            category_col: Name of category column
        
        Returns:
            Diversity score (0-1)
        """
        unique_categories = recommendations[category_col].nunique()
        total_items = len(recommendations)
        
        return unique_categories / min(total_items, total_items) if total_items > 0 else 0
    
    @staticmethod
    def genre_diversity(recommendations: pd.DataFrame) -> float:
        """Calculate diversity across genres"""
        unique_genres = 0
        for genres_str in recommendations.get('genre', []):
            if isinstance(genres_str, str):
                unique_genres += len(set(genres_str.split(',')))
        
        return unique_genres / len(recommendations) if len(recommendations) > 0 else 0


class NoveltyMetrics:
    """Metrics for measuring recommendation novelty/freshness"""
    
    @staticmethod
    def item_novelty(recommendations: pd.DataFrame,
                    interaction_df: pd.DataFrame,
                    popularity_col: str = 'popularity') -> float:
        """
        Item Novelty: How obscure/unpopular recommended items are
        Lower popularity = Higher novelty
        
        Args:
            recommendations: DataFrame with recommended items
            interaction_df: DataFrame with user interactions
            popularity_col: Name of popularity column
        
        Returns:
            Novelty score (0-1)
        """
        if len(recommendations) == 0:
            return 0
        
        # Normalize popularity scores
        if popularity_col in recommendations.columns:
            popularity = recommendations[popularity_col].values
            max_popularity = interaction_df[popularity_col].max() if popularity_col in interaction_df.columns else 100
            
            novelty = (1 - popularity / max_popularity).mean()
            return min(novelty, 1.0)
        
        return 0.5
    
    @staticmethod
    def temporal_novelty(recommendations: pd.DataFrame,
                        date_col: str = 'release_date') -> float:
        """
        Temporal Novelty: How recent recommended items are
        
        Args:
            recommendations: DataFrame with recommended items
            date_col: Name of date column
        
        Returns:
            Novelty score (0-1)
        """
        if date_col not in recommendations.columns:
            return 0.5
        
        # Convert to datetime
        dates = pd.to_datetime(recommendations[date_col], errors='coerce')
        dates = dates.dropna()
        
        if len(dates) == 0:
            return 0.5
        
        # Calculate recency
        max_date = dates.max()
        min_date = dates.min()
        date_range = (max_date - min_date).days
        
        avg_age = dates.apply(lambda x: (max_date - x).days).mean()
        
        novelty = 1 - (avg_age / max(date_range, 1))
        return max(min(novelty, 1.0), 0.0)


# ============================================================================
# COVERAGE METRICS
# ============================================================================

class CoverageMetrics:
    """Metrics for measuring catalog coverage"""
    
    @staticmethod
    def catalog_coverage(recommendations: List[int], 
                        catalog_size: int) -> float:
        """
        Catalog Coverage: Fraction of catalog items recommended
        
        Args:
            recommendations: List of recommended item IDs
            catalog_size: Total number of items in catalog
        
        Returns:
            Coverage score (0-1)
        """
        unique_items = len(set(recommendations))
        return unique_items / catalog_size if catalog_size > 0 else 0
    
    @staticmethod
    def gini_coefficient(item_frequencies: Dict[int, int]) -> float:
        """
        Gini Coefficient: Measures inequality in item recommendations
        0 = Perfect equality, 1 = Perfect inequality
        
        Args:
            item_frequencies: Dict of {item_id: recommendation_count}
        
        Returns:
            Gini coefficient (0-1)
        """
        if not item_frequencies:
            return 0
        
        frequencies = np.array(list(item_frequencies.values()))
        n = len(frequencies)
        
        if n == 0:
            return 0
        
        # Gini coefficient formula
        sorted_freq = np.sort(frequencies)
        cumsum = np.cumsum(sorted_freq)
        
        gini = (2 * np.sum((np.arange(1, n + 1)) * sorted_freq)) / (n * cumsum[-1]) - (n + 1) / n
        
        return max(0, min(gini, 1))


# ============================================================================
# SIMILARITY & SERENDIPITY METRICS
# ============================================================================

class SerendipityMetrics:
    """Metrics for measuring serendipity and unexpectedness"""
    
    @staticmethod
    def serendipity_score(recommendations: pd.DataFrame,
                         user_history: List[int],
                         user_preferences: Dict) -> float:
        """
        Serendipity: Balance between relevance and unexpectedness
        
        Args:
            recommendations: DataFrame with recommendations
            user_history: List of previously liked item IDs
            user_preferences: Dictionary of user preference weights
        
        Returns:
            Serendipity score (0-1)
        """
        if len(recommendations) == 0:
            return 0
        
        # Unexpectedness: How different from user history
        recommended_ids = set(recommendations['item_id'])
        history_ids = set(user_history)
        
        new_items = len(recommended_ids - history_ids)
        unexpectedness = new_items / len(recommendations) if len(recommendations) > 0 else 0
        
        # Balance with relevance (assuming scores are in recommendations)
        if 'score' in recommendations.columns:
            relevance = recommendations['score'].mean() / 100
        else:
            relevance = 0.5
        
        # Serendipity is high when both relevance AND unexpectedness are high
        serendipity = np.sqrt(relevance * unexpectedness)
        
        return serendipity
    
    @staticmethod
    def long_tail_ratio(recommendations: pd.DataFrame,
                       popularity_col: str = 'popularity') -> float:
        """
        Long-tail Ratio: Fraction of recommendations from long-tail items
        (less popular but more diverse content)
        
        Args:
            recommendations: DataFrame with recommendations
            popularity_col: Name of popularity column
        
        Returns:
            Ratio (0-1)
        """
        if popularity_col not in recommendations.columns or len(recommendations) == 0:
            return 0
        
        popularity = recommendations[popularity_col].values
        median_popularity = np.median(popularity)
        
        long_tail_items = np.sum(popularity < median_popularity)
        
        return long_tail_items / len(recommendations)


# ============================================================================
# RATING PREDICTION METRICS
# ============================================================================

class RatingMetrics:
    """Metrics for rating prediction accuracy"""
    
    @staticmethod
    def mean_absolute_error(true_ratings: np.ndarray, 
                           predicted_ratings: np.ndarray) -> float:
        """Mean Absolute Error for rating predictions"""
        return mean_absolute_error(true_ratings, predicted_ratings)
    
    @staticmethod
    def root_mean_squared_error(true_ratings: np.ndarray,
                               predicted_ratings: np.ndarray) -> float:
        """Root Mean Squared Error for rating predictions"""
        return np.sqrt(mean_squared_error(true_ratings, predicted_ratings))
    
    @staticmethod
    def rating_prediction_accuracy(true_ratings: np.ndarray,
                                   predicted_ratings: np.ndarray,
                                   tolerance: float = 0.5) -> float:
        """
        Accuracy: Fraction of predictions within tolerance
        
        Args:
            true_ratings: True rating values
            predicted_ratings: Predicted rating values
            tolerance: Acceptable prediction error
        
        Returns:
            Accuracy (0-1)
        """
        errors = np.abs(true_ratings - predicted_ratings)
        correct = np.sum(errors <= tolerance)
        return correct / len(true_ratings) if len(true_ratings) > 0 else 0


# ============================================================================
# COMPREHENSIVE EVALUATION
# ============================================================================

class ComprehensiveEvaluator:
    """Comprehensive recommendation system evaluator"""
    
    def __init__(self, recommendations: pd.DataFrame,
                 true_items: List[int],
                 interaction_df: pd.DataFrame,
                 catalog_size: int):
        self.recommendations = recommendations
        self.true_items = true_items
        self.interaction_df = interaction_df
        self.catalog_size = catalog_size
    
    def evaluate_all(self, k: int = 10) -> RecommendationMetrics:
        """
        Calculate all recommendation metrics
        
        Args:
            k: Number of top recommendations to consider
        
        Returns:
            RecommendationMetrics object with all scores
        """
        predicted_items = list(self.recommendations['item_id'].values[:k])
        
        # Ranking metrics
        precision = RankingMetrics.precision_at_k(self.true_items, predicted_items, k)
        recall = RankingMetrics.recall_at_k(self.true_items, predicted_items, k)
        ndcg = RankingMetrics.ndcg_at_k(self.true_items, predicted_items, k)
        map_score = RankingMetrics.map_at_k(self.true_items, predicted_items, k)
        
        # Rating metrics
        if 'score' in self.recommendations.columns:
            rmse = RatingMetrics.root_mean_squared_error(
                np.ones(len(self.recommendations[:k])) * 5,  # Assumed baseline
                self.recommendations[:k]['score'].values / 20  # Normalize to 0-5 scale
            )
            mae = RatingMetrics.mean_absolute_error(
                np.ones(len(self.recommendations[:k])) * 5,
                self.recommendations[:k]['score'].values / 20
            )
        else:
            rmse = mae = 0.5
        
        # Diversity metrics
        feature_cols = [col for col in self.recommendations.columns 
                       if col not in ['item_id', 'title', 'score']]
        
        if feature_cols and len(feature_cols) <= 5:
            try:
                diversity = DiversityMetrics.intra_list_diversity(
                    self.recommendations[:k], feature_cols[:5]
                )
            except:
                diversity = 0.5
        else:
            diversity = 0.5
        
        # Novelty metrics
        novelty = NoveltyMetrics.item_novelty(
            self.recommendations[:k],
            self.interaction_df
        )
        
        # Coverage metrics
        coverage = CoverageMetrics.catalog_coverage(
            list(self.recommendations['item_id'].values[:k]),
            self.catalog_size
        )
        
        # Serendipity
        serendipity = SerendipityMetrics.serendipity_score(
            self.recommendations[:k],
            [],
            {}
        )
        
        # Calculate F1-score
        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0
        
        return RecommendationMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1,
            ndcg=ndcg,
            map_score=map_score,
            rmse=rmse,
            mae=mae,
            coverage=coverage,
            diversity=diversity,
            novelty=novelty,
            serendipity=serendipity
        )


# ============================================================================
# REPORTING
# ============================================================================

class MetricsReporter:
    """Generate evaluation reports"""
    
    @staticmethod
    def generate_report(metrics: RecommendationMetrics) -> str:
        """Generate human-readable metrics report"""
        report = f"""
        ╔══════════════════════════════════════════════════════════╗
        ║       RECOMMENDATION SYSTEM EVALUATION REPORT             ║
        ╚══════════════════════════════════════════════════════════╝
        
        RANKING QUALITY:
        ├─ Precision@10:        {metrics.precision:.1%}
        ├─ Recall@10:           {metrics.recall:.1%}
        ├─ F1-Score:            {metrics.f1_score:.1%}
        ├─ NDCG@10:             {metrics.ndcg:.1%}
        └─ MAP@10:              {metrics.map_score:.1%}
        
        PREDICTION ACCURACY:
        ├─ RMSE:                {metrics.rmse:.4f}
        └─ MAE:                 {metrics.mae:.4f}
        
        CATALOG & DIVERSITY:
        ├─ Catalog Coverage:    {metrics.coverage:.1%}
        ├─ Diversity Score:     {metrics.diversity:.2f}
        └─ Novelty Score:       {metrics.novelty:.2f}
        
        USER EXPERIENCE:
        ├─ Serendipity:         {metrics.serendipity:.1%}
        """
        
        return report
    
    @staticmethod
    def metrics_to_dataframe(metrics: RecommendationMetrics) -> pd.DataFrame:
        """Convert metrics to DataFrame"""
        return pd.DataFrame({
            'Metric': [
                'Precision@10', 'Recall@10', 'F1-Score', 'NDCG@10', 'MAP@10',
                'RMSE', 'MAE', 'Coverage', 'Diversity', 'Novelty', 'Serendipity'
            ],
            'Score': [
                metrics.precision, metrics.recall, metrics.f1_score,
                metrics.ndcg, metrics.map_score, metrics.rmse, metrics.mae,
                metrics.coverage, metrics.diversity, metrics.novelty,
                metrics.serendipity
            ]
        })
