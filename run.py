from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
import os
from backend.resume_builder import ResumeBuilder
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from backend.resume_parser import ResumeParser
from backend.skill_extractor import SkillExtractor
from backend.score_calculator import ScoreCalculator
from backend.suggestions import ResumeSuggestions
from backend.ats_checker import ATSChecker
from backend.jd_matcher import JDMatcher
from backend.cover_letter import CoverLetterGenerator
from backend.pdf_generator import PDFGenerator
from backend.database import Database
from backend.ml_predictor import MLScorePredictor
from backend.salary_predictor import SalaryPredictor
from backend.interview_questions import InterviewQuestionGenerator
from backend.advanced_features import AdvancedFeatures
from backend.email_sender import EmailSender
from backend.bulk_analyzer import BulkAnalyzer


import uuid
import traceback
import json

load_dotenv()

app = Flask(__name__, 
            template_folder='frontend/templates',
            static_folder='frontend/static')

app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REPORT_FOLDER'] = 'reports'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['DEBUG'] = os.getenv('DEBUG', 'True') == 'True'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

# Initialize components
resume_parser = ResumeParser()
skill_extractor = SkillExtractor()
score_calculator = ScoreCalculator()
suggestion_generator = ResumeSuggestions()
ats_checker = ATSChecker()
jd_matcher = JDMatcher()
cover_letter_generator = CoverLetterGenerator()
pdf_generator = PDFGenerator()
MONGODB_URI = 'mongodb+srv://sneha_jaiswal00:Sneha1905@cluster0.opdtagu.mongodb.net/?appName=Cluster0'
database = Database(MONGODB_URI)
ml_predictor = MLScorePredictor()
salary_predictor = SalaryPredictor()
interview_generator = InterviewQuestionGenerator()
advanced_features = AdvancedFeatures()
email_sender = EmailSender()
bulk_analyzer = BulkAnalyzer(resume_parser, skill_extractor, score_calculator)
resume_builder = ResumeBuilder()



# ==================== PAGE ROUTES ====================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result')
def show_result():
    if 'analysis_result' not in session:
        return redirect(url_for('index'))
    result = session['analysis_result']
    return render_template('result.html', result=result)

@app.route('/compare')
def compare_page():
    return render_template('compare.html')

@app.route('/jd-match')
def jd_match_page():
    return render_template('jd_match.html')

@app.route('/bulk-analyze-page')
def bulk_analyze_page():
    return render_template('bulk_analyze.html')



@app.route('/resume-builder')
def resume_builder_page():
    return render_template('resume_builder.html')



@app.route('/templates')
def templates_page():
    return render_template('templates.html')

# ==================== ANALYSIS ROUTES ====================

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        target_job_role = request.form.get('job_role', '')
        user_email = request.form.get('user_email', 'anonymous')
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        resume_text = resume_parser.extract_text(filepath)
        extracted_skills = skill_extractor.extract_skills(resume_text)
        scores = score_calculator.calculate_total_score(resume_text, extracted_skills)
        suggestions = suggestion_generator.generate_suggestions(scores, extracted_skills, resume_text)
        contact_info = resume_parser.extract_contact_info(resume_text)
        career_predictions = score_calculator.predict_career_roles(resume_text, extracted_skills)
        ats_result = ats_checker.check_ats_compatibility(resume_text, filename)
        
        # Calculate target role match
        target_role_match = None
        if target_job_role:
            target_role_match = score_calculator.calculate_target_role_match(resume_text, extracted_skills, target_job_role)
        
        session['analysis_result'] = {
            'user_email': user_email,
            'resume_text': resume_text,
            'extracted_skills': extracted_skills,
            'scores': scores,
            'suggestions': suggestions,
            'contact_info': contact_info,
            'career_predictions': career_predictions,
            'ats_result': ats_result,
            'filename': filename,
            'target_job_role': target_job_role,
            'target_role_match': target_role_match
        }
        
       
        
        database.save_analysis({
            'filename': filename,
            'resume_text': resume_text,
            'total_score': scores['total_score'],
            'grade': scores['grade'],
            'skills_count': sum(len(s) for s in extracted_skills.values()),
            'technical_skills': extracted_skills['technical_skills'],
            'soft_skills': extracted_skills['soft_skills'],
            'domain_skills': extracted_skills['domain_skills'],
            'career_predictions': career_predictions,
            'ats_score': ats_result['ats_score'],
            'ats_rating': ats_result['rating'],
            'suggestions': suggestions
        })
        
        os.remove(filepath)
        return jsonify({'success': True, 'redirect': '/result'})
    
    except Exception as e:
        print("\n=== ERROR IN /analyze ===")
        traceback.print_exc()
        print("=========================\n")
        return jsonify({'error': str(e)}), 500

@app.route('/compare', methods=['POST'])
def compare_resumes():
    try:
        if 'resume1' not in request.files or 'resume2' not in request.files:
            return jsonify({'error': 'Please upload both resumes'}), 400
        
        file1 = request.files['resume1']
        file2 = request.files['resume2']
        
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], f"1_{filename1}")
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], f"2_{filename2}")
        file1.save(filepath1)
        file2.save(filepath2)
        
        text1 = resume_parser.extract_text(filepath1)
        text2 = resume_parser.extract_text(filepath2)
        
        skills1 = skill_extractor.extract_skills(text1)
        skills2 = skill_extractor.extract_skills(text2)
        
        scores1 = score_calculator.calculate_total_score(text1, skills1)
        scores2 = score_calculator.calculate_total_score(text2, skills2)
        
        os.remove(filepath1)
        os.remove(filepath2)
        
        result = {
            'resume1': {
                'filename': filename1,
                'total_score': scores1['total_score'],
                'grade': scores1['grade'],
                'skills_count': sum(len(s) for s in skills1.values())
            },
            'resume2': {
                'filename': filename2,
                'total_score': scores2['total_score'],
                'grade': scores2['grade'],
                'skills_count': sum(len(s) for s in skills2.values())
            },
            'winner': 'resume1' if scores1['total_score'] > scores2['total_score'] else 'resume2'
        }
        
        return jsonify(result)
    
    except Exception as e:
        print("\n=== ERROR IN /compare ===")
        traceback.print_exc()
        print("=========================\n")
        return jsonify({'error': str(e)}), 500

@app.route('/jd-match', methods=['POST'])
def jd_match():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume uploaded'}), 400
        
        file = request.files['resume']
        jd_text = request.form.get('jd_text', '')
        
        if not jd_text:
            return jsonify({'error': 'Please paste job description'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        resume_text = resume_parser.extract_text(filepath)
        match_result = jd_matcher.match_with_jd(resume_text, jd_text)
        
        os.remove(filepath)
        return jsonify(match_result)
    
    except Exception as e:
        print("\n=== ERROR IN /jd-match ===")
        traceback.print_exc()
        print("===========================\n")
        return jsonify({'error': str(e)}), 500

@app.route('/bulk-analyze', methods=['POST'])
def bulk_analyze():
    try:
        files = request.files.getlist('resumes')
        if not files:
            return jsonify({'error': 'No files uploaded'}), 400
        
        results = bulk_analyzer.analyze_bulk(files, app.config['UPLOAD_FOLDER'])
        
        report_dir = os.path.join(app.config['REPORT_FOLDER'], 'bulk')
        os.makedirs(report_dir, exist_ok=True)
        excel_path = os.path.join(report_dir, 'bulk_analysis.xlsx')
        bulk_analyzer.generate_excel(results, excel_path)
        
        database.save_bulk_analysis('Bulk Analysis', results)
        
        return jsonify({
            'success': True,
            'results': results,
            'excel_url': '/download-bulk-report'
        })
    
    except Exception as e:
        print("\n=== ERROR IN /bulk-analyze ===")
        traceback.print_exc()
        print("=============================\n")
        return jsonify({'error': str(e)}), 500

@app.route('/download-bulk-report')
def download_bulk_report():
    report_path = os.path.join(app.config['REPORT_FOLDER'], 'bulk', 'bulk_analysis.xlsx')
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True, download_name='bulk_analysis_report.xlsx')
    return jsonify({'error': 'Report not found'}), 404

# ==================== API ROUTES ====================

@app.route('/api/predict-score', methods=['POST'])
def predict_score():
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        extracted_skills = data.get('extracted_skills', {})
        prediction = ml_predictor.predict_score(resume_text, extracted_skills)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/salary-prediction', methods=['POST'])
def predict_salary():
    try:
        data = request.get_json()
        role = data.get('role', '')
        experience = data.get('experience_years', 0)
        skills = data.get('skills', [])
        location = data.get('location', 'remote')
        prediction = salary_predictor.predict_salary(role, experience, skills, location)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview-questions', methods=['POST'])
def get_interview_questions():
    try:
        data = request.get_json()
        skills = data.get('skills', [])
        experience = data.get('experience_years', 0)
        questions = interview_generator.generate_questions(skills, experience)
        return jsonify(questions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skill-gap', methods=['POST'])
def skill_gap():
    try:
        data = request.get_json()
        current_skills = data.get('skills', [])
        target_role = data.get('target_role', '')
        analysis = advanced_features.skill_gap_analysis(current_skills, target_role)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/certifications', methods=['POST'])
def get_certifications():
    try:
        data = request.get_json()
        role = data.get('role', '')
        certs = advanced_features.suggest_certifications([], role)
        return jsonify(certs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/industry-analysis', methods=['POST'])
def industry_analysis():
    try:
        data = request.get_json()
        text = data.get('text', '')
        skills = data.get('skills', [])
        industry = data.get('industry', 'IT')
        result = advanced_features.industry_analysis(text, skills, industry)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/grammar-check', methods=['POST'])
def grammar_check():
    try:
        data = request.get_json()
        text = data.get('text', '')
        result = advanced_features.check_grammar(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/readability', methods=['POST'])
def check_readability():
    try:
        data = request.get_json()
        text = data.get('text', '')
        result = advanced_features.check_readability(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/achievements', methods=['POST'])
def check_achievements():
    try:
        data = request.get_json()
        text = data.get('text', '')
        result = advanced_features.quantify_achievements(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history')
def get_history():
    try:
        history = database.get_analysis_history(limit=10)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    try:
        stats = database.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        output_path = os.path.join(app.config['REPORT_FOLDER'], 'generated_resume.pdf')
        resume_builder.generate_resume(data, output_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download-generated-resume')
def download_generated_resume():
    path = os.path.join(app.config['REPORT_FOLDER'], 'generated_resume.pdf')
    if os.path.exists(path):
        return send_file(path, as_attachment=True, download_name='my_resume.pdf')
    return jsonify({'error': 'Resume not found'}), 404

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    try:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_role = data.get('job_role', '')
        extracted_skills = data.get('extracted_skills', {})
        cover_letter = cover_letter_generator.generate_cover_letter(resume_text, extracted_skills, job_role)
        return jsonify({'cover_letter': cover_letter})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-report')
def download_report():
    try:
        if 'analysis_result' not in session:
            return redirect(url_for('index'))
        result = session['analysis_result']
        report_path = os.path.join(app.config['REPORT_FOLDER'], 'resume_report.pdf')
        pdf_generator.generate_report(result, report_path)
        return send_file(report_path, as_attachment=True, download_name='resume_analysis_report.pdf')
    except Exception as e:
        print("\n=== ERROR IN /download-report ===")
        traceback.print_exc()
        print("================================\n")
        return jsonify({'error': str(e)}), 500






if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True') == 'True'
    app.run(debug=debug, host='127.0.0.1', port=port)