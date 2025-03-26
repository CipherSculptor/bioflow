# BioFlow - Blood Parameter Prediction

BioFlow is a web application that uses machine learning to predict blood parameters based on permittivity values and blood group.

## Features

- Predicts RBC count, WBC count, platelets, and hemoglobin levels
- User-friendly interface with form-based input
- Supports A+, B+, and O+ blood groups
- Generates PDF reports of predictions
- Responsive design that works on all devices

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Data Visualization**: PDF generation with jsPDF

## Installation

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bioflow.git
cd bioflow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the API server:
```bash
python api.py
```

4. In a new terminal, start the web server:
```bash
python -m http.server 8000
```

5. Open your browser and navigate to:
```
http://localhost:8000/
```

## Usage

1. Log in (any credentials work in demo mode)
2. Enter your details:
   - Name
   - Age
   - Gender
   - Blood Group (A+, B+, or O+ only)
   - Permittivity Value (range 60-75 for best results)
3. Click "Evaluate" to see predictions
4. View your results or generate a PDF report

## Project Structure

- `index.html` - Login page
- `dashboard.html` - Form for entering parameters
- `results.html` - Displays prediction results
- `api.py` - Flask API for machine learning predictions
- `models/` - Trained machine learning models

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed for educational and research purposes
- Uses a dataset of blood parameters and permittivity values 