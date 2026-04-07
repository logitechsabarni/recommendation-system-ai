"""
PersonaAI - Comprehensive Examples & Demos
===========================================
Real-world usage examples for all features
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from recommendation_system import (
    RecommendationEngine,
    PersonalizationAnalyzer
)
from analytics import (
    RankingMetrics,
    DiversityMetrics,
    NoveltyMetrics,
    ComprehensiveEvaluator,
    MetricsReporter
)


# ============================================================================
# EXAMPLE 1: Basic Recommendations
# ============================================================================

def example_basic_recommendations():
    """Example 1: Get basic recommendations for a user"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Recommendations")
    print("="*70)
    
    # Initialize recommendation engine
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    user_id = 1
    print(f"\nGenerating recommendations for User {user_id}...")
    
    # Get recommendations using different algorithms
    print("\n📊 Collaborative Filtering Recommendations:")
    collab_recs = engine.collaborative_filtering(user_id, n_recommendations=5)
    print(collab_recs[['title', 'category', 'rating', 'score']].to_string())
    
    print("\n📊 Content-Based Recommendations:")
    content_recs = engine.content_based_filtering(user_id, n_recommendations=5)
    print(content_recs[['title', 'category', 'rating', 'score']].to_string())
    
    print("\n📊 Hybrid Recommendations (60/40 weight):")
    hybrid_recs = engine.hybrid_recommendation(
        user_id, 
        n_recommendations=5,
        collab_weight=0.6,
        content_weight=0.4
    )
    print(hybrid_recs[['title', 'category', 'rating', 'score']].to_string())
    
    print("\n📊 Trending Items:")
    trending = engine.trending_items(n_items=5)
    print(trending[['title', 'category', 'rating', 'score']].to_string())


# ============================================================================
# EXAMPLE 2: User Profile Analysis
# ============================================================================

def example_user_profile_analysis():
    """Example 2: Analyze user preferences and behavior"""
    print("\n" + "="*70)
    print("EXAMPLE 2: User Profile Analysis")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    analyzer = PersonalizationAnalyzer(engine)
    
    # Analyze multiple users
    for user_id in [1, 5, 10]:
        print(f"\n👤 User {user_id} Profile:")
        print("-" * 50)
        
        profile = analyzer.get_user_profile(user_id)
        
        if profile:
            print(f"  Total Interactions:     {profile['total_interactions']}")
            print(f"  Average Rating:         {profile['avg_rating']:.2f} ★")
            print(f"  Favorite Category:      {profile['favorite_category']}")
            print(f"  Favorite Genre:         {profile['favorite_genre']}")
            print(f"  Average Item Rating:    {profile['avg_item_rating']:.2f} ★")
            print(f"  Activity Level:         {profile['activity_level']}")
            print(f"  Items Reviewed:         {profile['items_reviewed']}")
            
            # Category preferences
            prefs = analyzer.get_category_preferences(user_id)
            print(f"\n  Category Preferences:")
            for _, row in prefs.iterrows():
                bar_length = int(row['percentage'] / 5)
                bar = "█" * bar_length
                print(f"    {row['category']:12} {row['percentage']:5.1f}% {bar}")


# ============================================================================
# EXAMPLE 3: Algorithm Comparison
# ============================================================================

def example_algorithm_comparison():
    """Example 3: Compare different recommendation algorithms"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Algorithm Comparison")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    user_id = 1
    n_recs = 10
    
    print(f"\nComparing algorithms for User {user_id} (top {n_recs} recommendations)")
    print("-" * 70)
    
    # Get recommendations from all algorithms
    algorithms = {
        'Collaborative': engine.collaborative_filtering(user_id, n_recs),
        'Content-Based': engine.content_based_filtering(user_id, n_recs),
        'Hybrid (60/40)': engine.hybrid_recommendation(user_id, n_recs, 0.6),
        'Trending': engine.trending_items(n_recs)
    }
    
    # Compare metrics
    print("\nAlgorithm Performance Summary:")
    print("-" * 70)
    
    metrics_comparison = []
    
    for algo_name, recs in algorithms.items():
        if len(recs) > 0:
            avg_score = recs['score'].mean()
            score_std = recs['score'].std()
            max_score = recs['score'].max()
            
            metrics_comparison.append({
                'Algorithm': algo_name,
                'Avg Score': f"{avg_score:.2f}",
                'Std Dev': f"{score_std:.2f}",
                'Max Score': f"{max_score:.2f}",
                'Count': len(recs)
            })
    
    comparison_df = pd.DataFrame(metrics_comparison)
    print(comparison_df.to_string(index=False))
    
    # Show recommendation overlap
    print("\n\nRecommendation Overlap Analysis:")
    print("-" * 70)
    
    for i, (algo1, recs1) in enumerate(algorithms.items()):
        items1 = set(recs1['item_id'].values[:5])
        
        for algo2, recs2 in list(algorithms.items())[i+1:]:
            items2 = set(recs2['item_id'].values[:5])
            overlap = len(items1 & items2)
            
            print(f"{algo1:15} ∩ {algo2:15} = {overlap} items (out of 5)")


# ============================================================================
# EXAMPLE 4: Evaluation Metrics
# ============================================================================

def example_evaluation_metrics():
    """Example 4: Calculate and display evaluation metrics"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Evaluation Metrics")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    # Define some ground truth items for user 1
    user_id = 1
    true_items = [1, 5, 12, 23, 35]  # Items we assume are relevant
    
    # Get recommendations
    hybrid_recs = engine.hybrid_recommendation(user_id, n_recommendations=10)
    predicted_items = list(hybrid_recs['item_id'].values)
    
    print(f"\nEvaluating recommendations for User {user_id}")
    print("-" * 70)
    
    # Calculate ranking metrics
    print("\nRanking Metrics:")
    print("-" * 70)
    
    precision_5 = RankingMetrics.precision_at_k(true_items, predicted_items, k=5)
    precision_10 = RankingMetrics.precision_at_k(true_items, predicted_items, k=10)
    
    recall_5 = RankingMetrics.recall_at_k(true_items, predicted_items, k=5)
    recall_10 = RankingMetrics.recall_at_k(true_items, predicted_items, k=10)
    
    ndcg_5 = RankingMetrics.ndcg_at_k(true_items, predicted_items, k=5)
    ndcg_10 = RankingMetrics.ndcg_at_k(true_items, predicted_items, k=10)
    
    map_5 = RankingMetrics.map_at_k(true_items, predicted_items, k=5)
    map_10 = RankingMetrics.map_at_k(true_items, predicted_items, k=10)
    
    mrr_5 = RankingMetrics.mrr_at_k(true_items, predicted_items, k=5)
    
    print(f"Precision@5:     {precision_5:.1%}")
    print(f"Precision@10:    {precision_10:.1%}")
    print(f"Recall@5:        {recall_5:.1%}")
    print(f"Recall@10:       {recall_10:.1%}")
    print(f"NDCG@5:          {ndcg_5:.1%}")
    print(f"NDCG@10:         {ndcg_10:.1%}")
    print(f"MAP@5:           {map_5:.1%}")
    print(f"MAP@10:          {map_10:.1%}")
    print(f"MRR@5:           {mrr_5:.1%}")
    
    # Diversity metrics
    print("\nDiversity Metrics:")
    print("-" * 70)
    
    try:
        diversity = DiversityMetrics.category_diversity(hybrid_recs)
        print(f"Category Diversity: {diversity:.2f}")
    except:
        print("Category Diversity: Could not calculate")
    
    # Novelty metrics
    print("\nNovelty Metrics:")
    print("-" * 70)
    
    novelty = NoveltyMetrics.item_novelty(hybrid_recs, engine.interactions_df)
    print(f"Item Novelty:     {novelty:.2f}")


# ============================================================================
# EXAMPLE 5: Cold Start Problem Handling
# ============================================================================

def example_cold_start_handling():
    """Example 5: Handle new users and items (cold start problem)"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Cold Start Problem Handling")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    print("\nScenario 1: New User (No interaction history)")
    print("-" * 70)
    
    # New user with no interactions
    new_user_id = 999
    user_interactions = engine.interactions_df[
        engine.interactions_df['user_id'] == new_user_id
    ]
    
    print(f"User {new_user_id} interactions: {len(user_interactions)}")
    print("\nStrategy: Use trending items as recommendations")
    
    trending = engine.trending_items(n_items=5)
    print(trending[['title', 'category', 'rating']].to_string())
    
    print("\n\nScenario 2: New Item (No rating history)")
    print("-" * 70)
    
    # New item with no interactions
    new_item_id = 999
    item_interactions = engine.interactions_df[
        engine.interactions_df['item_id'] == new_item_id
    ]
    
    print(f"Item {new_item_id} interactions: {len(item_interactions)}")
    print("\nStrategy: Use content-based similarity with existing items")
    
    # Find similar items based on content
    sample_user = 1
    content_recs = engine.content_based_filtering(sample_user, n_recommendations=5)
    print(content_recs[['title', 'category', 'rating']].to_string())


# ============================================================================
# EXAMPLE 6: Personalization & Preference Learning
# ============================================================================

def example_personalization():
    """Example 6: Advanced personalization and preference learning"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Personalization & Preference Learning")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    analyzer = PersonalizationAnalyzer(engine)
    
    print("\nLearning user preferences over time...")
    print("-" * 70)
    
    user_id = 1
    
    # Get user's rated items with timestamps
    user_ratings = engine.interactions_df[
        engine.interactions_df['user_id'] == user_id
    ].sort_values('timestamp')
    
    print(f"\nUser {user_id}'s recent activity:")
    
    for idx, (_, rating) in enumerate(user_ratings.tail(5).iterrows(), 1):
        item = engine.items_df[engine.items_df['item_id'] == rating['item_id']].iloc[0]
        print(f"  {idx}. {item['title']} - Rating: {rating['rating']:.1f} ★")
    
    # Analyze preference evolution
    print("\n\nPreference Analysis:")
    print("-" * 70)
    
    profile = analyzer.get_user_profile(user_id)
    
    print(f"\nLearned Preferences:")
    print(f"  Favorite Category:    {profile['favorite_category']}")
    print(f"  Favorite Genre:       {profile['favorite_genre']}")
    print(f"  Average Rating Given: {profile['avg_rating']:.2f} ★")
    print(f"  Engagement:           {profile['activity_level']}")
    
    # Recommendation personalization
    print("\n\nPersonalized Recommendations:")
    print("-" * 70)
    
    # Weight hybrid algorithm based on engagement
    if profile['activity_level'] == 'High':
        collab_weight = 0.7  # Trust collaborative filtering more
    elif profile['activity_level'] == 'Medium':
        collab_weight = 0.6  # Balanced approach
    else:
        collab_weight = 0.4  # Trust content-based more
    
    print(f"\nBased on {profile['activity_level']} engagement,")
    print(f"using weights: Collab={collab_weight}, Content={1-collab_weight}")
    
    recs = engine.hybrid_recommendation(
        user_id,
        n_recommendations=5,
        collab_weight=collab_weight
    )
    
    print(f"\nTop Recommendations:")
    for idx, (_, rec) in enumerate(recs.iterrows(), 1):
        print(f"  {idx}. {rec['title']} - Match: {rec['score']:.0f}%")


# ============================================================================
# EXAMPLE 7: Diversity & Serendipity Optimization
# ============================================================================

def example_diversity_serendipity():
    """Example 7: Optimize for diversity and serendipity"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Diversity & Serendipity Optimization")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    user_id = 1
    
    print("\nShowing recommendations with different optimization goals")
    print("-" * 70)
    
    # Standard recommendations
    print("\n1️⃣  STANDARD RECOMMENDATIONS (Highest Score):")
    standard_recs = engine.hybrid_recommendation(user_id, n_recommendations=10)
    
    categories = standard_recs['category'].unique()
    print(f"   Unique categories: {len(categories)} - {', '.join(categories[:5])}")
    
    for idx, (_, rec) in enumerate(standard_recs.head(5).iterrows(), 1):
        print(f"   {idx}. {rec['title']} ({rec['category']}) - {rec['score']:.0f}%")
    
    # Diverse recommendations
    print("\n2️⃣  DIVERSE RECOMMENDATIONS (Different categories):")
    
    diverse_recs = standard_recs.copy()
    selected_cats = set()
    diverse_selection = []
    
    for _, rec in diverse_recs.iterrows():
        if rec['category'] not in selected_cats:
            diverse_selection.append(rec)
            selected_cats.add(rec['category'])
            if len(diverse_selection) >= 5:
                break
    
    diverse_selection_df = pd.DataFrame(diverse_selection)
    
    categories = diverse_selection_df['category'].unique()
    print(f"   Unique categories: {len(categories)} - {', '.join(categories)}")
    
    for idx, rec in enumerate(diverse_selection, 1):
        print(f"   {idx}. {rec['title']} ({rec['category']}) - {rec['score']:.0f}%")
    
    # Long-tail recommendations
    print("\n3️⃣  LONG-TAIL RECOMMENDATIONS (Lesser-known items):")
    
    long_tail_recs = standard_recs.copy()
    long_tail_recs = long_tail_recs.nsmallest(5, 'popularity')
    
    print(f"   Average popularity: {long_tail_recs['popularity'].mean():.2f}")
    
    for idx, (_, rec) in enumerate(long_tail_recs.iterrows(), 1):
        print(f"   {idx}. {rec['title']} - Popularity: {rec['popularity']:.2f}")


# ============================================================================
# EXAMPLE 8: Batch Recommendations for Multiple Users
# ============================================================================

def example_batch_recommendations():
    """Example 8: Generate recommendations for multiple users"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Batch Recommendations for Multiple Users")
    print("="*70)
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    print("\nGenerating recommendations for 10 users...")
    print("-" * 70)
    
    batch_results = []
    
    for user_id in range(1, 11):
        recs = engine.hybrid_recommendation(user_id, n_recommendations=3)
        
        if len(recs) > 0:
            top_rec = recs.iloc[0]
            batch_results.append({
                'User': user_id,
                'Top Recommendation': top_rec['title'],
                'Category': top_rec['category'],
                'Score': f"{top_rec['score']:.0f}%"
            })
    
    batch_df = pd.DataFrame(batch_results)
    print("\n" + batch_df.to_string(index=False))
    
    # Summary statistics
    print("\n\nBatch Processing Summary:")
    print("-" * 70)
    print(f"Users processed:      {len(batch_results)}")
    print(f"Total recommendations: {len(batch_results) * 3}")
    print(f"Average top score:     {np.mean([float(r['Score'].rstrip('%')) for r in batch_results]):.0f}%")


# ============================================================================
# EXAMPLE 9: Real-time Performance Monitoring
# ============================================================================

def example_performance_monitoring():
    """Example 9: Monitor recommendation system performance"""
    print("\n" + "="*70)
    print("EXAMPLE 9: Real-time Performance Monitoring")
    print("="*70)
    
    import time
    
    engine = RecommendationEngine()
    engine.generate_sample_data()
    
    algorithms = ['Collaborative', 'Content-Based', 'Hybrid', 'Trending']
    user_ids = [1, 5, 10, 15, 20]
    
    print("\nBenchmarking recommendation algorithms...")
    print("-" * 70)
    
    results = []
    
    for algo in algorithms:
        times = []
        
        for user_id in user_ids:
            start = time.time()
            
            if algo == 'Collaborative':
                engine.collaborative_filtering(user_id, 10)
            elif algo == 'Content-Based':
                engine.content_based_filtering(user_id, 10)
            elif algo == 'Hybrid':
                engine.hybrid_recommendation(user_id, 10)
            else:  # Trending
                engine.trending_items(10)
            
            elapsed = (time.time() - start) * 1000  # Convert to ms
            times.append(elapsed)
        
        results.append({
            'Algorithm': algo,
            'Avg Time (ms)': f"{np.mean(times):.2f}",
            'Min (ms)': f"{np.min(times):.2f}",
            'Max (ms)': f"{np.max(times):.2f}",
            'Std Dev (ms)': f"{np.std(times):.2f}"
        })
    
    performance_df = pd.DataFrame(results)
    print("\n" + performance_df.to_string(index=False))
    
    print("\n\nPerformance Summary:")
    print("-" * 70)
    print("✅ All algorithms completed successfully")
    print(f"✅ Total users benchmarked: {len(user_ids)}")
    print(f"✅ Total algorithms tested: {len(algorithms)}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all examples"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║          PersonaAI - Comprehensive Examples & Demos       ║
║                                                            ║
║     Intelligent Recommendation System with Machine        ║
║               Learning & AI Personalization               ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    examples = [
        ("Basic Recommendations", example_basic_recommendations),
        ("User Profile Analysis", example_user_profile_analysis),
        ("Algorithm Comparison", example_algorithm_comparison),
        ("Evaluation Metrics", example_evaluation_metrics),
        ("Cold Start Handling", example_cold_start_handling),
        ("Personalization", example_personalization),
        ("Diversity & Serendipity", example_diversity_serendipity),
        ("Batch Recommendations", example_batch_recommendations),
        ("Performance Monitoring", example_performance_monitoring),
    ]
    
    print("\nAvailable Examples:")
    print("-" * 70)
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\n0. Run All Examples")
    print("Q. Quit")
    
    while True:
        choice = input("\nSelect example (0-9, Q): ").strip().upper()
        
        if choice == 'Q':
            print("\nGoodbye! 👋")
            break
        elif choice == '0':
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
            input("\n\nPress Enter to continue...")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            try:
                examples[int(choice) - 1][1]()
            except Exception as e:
                print(f"\n❌ Error: {e}")
            input("\n\nPress Enter to continue...")
        else:
            print("Invalid selection. Please try again.")


if __name__ == '__main__':
    main()
