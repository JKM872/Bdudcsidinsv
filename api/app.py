"""
Flask API Server for Sports Prediction Dashboard
Provides REST endpoints for accessing prediction data from Supabase
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from supabase_manager import SupabaseManager

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize Supabase manager
db = SupabaseManager()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


@app.route('/api/predictions/recent', methods=['GET'])
def get_recent_predictions():
    """
    Get recent predictions
    Query params:
    - days: number of days to look back (default: 7)
    - sport: filter by sport (optional)
    - qualified: filter qualified only (optional, default: false)
    """
    try:
        days = request.args.get('days', 7, type=int)
        sport = request.args.get('sport', None)
        qualified_only = request.args.get('qualified', 'false').lower() == 'true'
        
        # Build query
        query = db.client.table('predictions').select('*')
        
        # Date filter
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        query = query.gte('match_date', since_date)
        
        # Sport filter
        if sport:
            query = query.eq('sport', sport)
        
        # Qualified filter
        if qualified_only:
            query = query.eq('qualifies', True)
        
        # Order by date descending
        query = query.order('match_date', desc=True).order('match_time', desc=True)
        
        response = query.execute()
        
        return jsonify({
            'success': True,
            'count': len(response.data),
            'predictions': response.data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predictions/stats', methods=['GET'])
def get_statistics():
    """
    Get overall statistics
    Query params:
    - days: number of days to look back (default: 30)
    """
    try:
        days = request.args.get('days', 30, type=int)
        
        # Get all predictions in time range
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        response = db.client.table('predictions').select('*').gte('match_date', since_date).execute()
        
        predictions = response.data
        total = len(predictions)
        qualified = sum(1 for p in predictions if p.get('qualifies'))
        with_results = sum(1 for p in predictions if p.get('actual_result'))
        
        # Calculate accuracy by sport
        sports_stats = {}
        for pred in predictions:
            sport = pred.get('sport', 'unknown')
            if sport not in sports_stats:
                sports_stats[sport] = {'total': 0, 'qualified': 0, 'with_results': 0}
            
            sports_stats[sport]['total'] += 1
            if pred.get('qualifies'):
                sports_stats[sport]['qualified'] += 1
            if pred.get('actual_result'):
                sports_stats[sport]['with_results'] += 1
        
        return jsonify({
            'success': True,
            'period_days': days,
            'total_predictions': total,
            'qualified_predictions': qualified,
            'predictions_with_results': with_results,
            'by_sport': sports_stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/accuracy', methods=['GET'])
def get_accuracy():
    """
    Get accuracy statistics for all sources
    Query params:
    - days: number of days to look back (default: 30)
    """
    try:
        days = request.args.get('days', 30, type=int)
        
        # Get accuracy from Supabase manager
        accuracy_data = db.get_all_sources_accuracy(days=days)
        
        return jsonify({
            'success': True,
            'period_days': days,
            'sources': accuracy_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predictions/today', methods=['GET'])
def get_today_predictions():
    """Get predictions for today"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        
        response = db.client.table('predictions').select('*').eq('match_date', today).order('match_time').execute()
        
        return jsonify({
            'success': True,
            'date': today,
            'count': len(response.data),
            'predictions': response.data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predictions/upcoming', methods=['GET'])
def get_upcoming_predictions():
    """Get upcoming predictions (next 7 days)"""
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        response = db.client.table('predictions').select('*')\
            .gte('match_date', today)\
            .lte('match_date', next_week)\
            .eq('qualifies', True)\
            .order('match_date')\
            .order('match_time')\
            .execute()
        
        # Group by date
        by_date = {}
        for pred in response.data:
            date = pred['match_date']
            if date not in by_date:
                by_date[date] = []
            by_date[date].append(pred)
        
        return jsonify({
            'success': True,
            'start_date': today,
            'end_date': next_week,
            'total_count': len(response.data),
            'by_date': by_date
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predictions/<int:prediction_id>', methods=['GET'])
def get_prediction_detail(prediction_id):
    """Get detailed information about a specific prediction"""
    try:
        response = db.client.table('predictions').select('*').eq('id', prediction_id).execute()
        
        if not response.data:
            return jsonify({
                'success': False,
                'error': 'Prediction not found'
            }), 404
        
        return jsonify({
            'success': True,
            'prediction': response.data[0]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/predictions/<int:prediction_id>/result', methods=['POST'])
def update_prediction_result(prediction_id):
    """
    Update the result of a prediction
    Body: {actual_result: '1'/'X'/'2', home_score: int, away_score: int}
    """
    try:
        data = request.json
        
        success = db.update_match_result(
            match_id=prediction_id,
            actual_result=data.get('actual_result'),
            home_score=data.get('home_score'),
            away_score=data.get('away_score')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Result updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update result'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/consensus', methods=['GET'])
def get_consensus_picks():
    """
    Get consensus picks (matches where multiple sources agree)
    Query params:
    - days: number of days to look back (default: 7)
    - min_agreement: minimum sources agreeing (2-4, default: 3)
    """
    try:
        days = request.args.get('days', 7, type=int)
        min_agreement = request.args.get('min_agreement', 3, type=int)
        
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        response = db.client.table('predictions').select('*')\
            .gte('match_date', since_date)\
            .eq('qualifies', True)\
            .execute()
        
        # Calculate consensus for each prediction
        consensus_picks = []
        for pred in response.data:
            agreement_count = 0
            sources_agreeing = []
            
            # Check each source
            if pred.get('livesport_win_rate', 0) >= 60:
                agreement_count += 1
                sources_agreeing.append('LiveSport')
            
            if pred.get('forebet_prediction') == '1':
                agreement_count += 1
                sources_agreeing.append('Forebet')
            
            if pred.get('sofascore_home_win_prob', 0) > pred.get('sofascore_away_win_prob', 0):
                agreement_count += 1
                sources_agreeing.append('SofaScore')
            
            if pred.get('gemini_recommendation') in ['HIGH', 'LOCK']:
                agreement_count += 1
                sources_agreeing.append('Gemini')
            
            if agreement_count >= min_agreement:
                pred['consensus_count'] = agreement_count
                pred['sources_agreeing'] = sources_agreeing
                consensus_picks.append(pred)
        
        # Sort by consensus count (highest first)
        consensus_picks.sort(key=lambda x: x['consensus_count'], reverse=True)
        
        return jsonify({
            'success': True,
            'period_days': days,
            'min_agreement': min_agreement,
            'count': len(consensus_picks),
            'picks': consensus_picks
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("🚀 Starting Sports Prediction API Server...")
    print("📊 Dashboard: http://localhost:5000")
    print("🔍 API Docs: http://localhost:5000/api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
