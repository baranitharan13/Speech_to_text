# Speech-to-Text Conversion Model Using Pre-Trained APIs & Clustering

This project implements a Speech-to-Text (STT) system using **Google Cloud Speech-to-Text API**, integrated with **K-Means clustering** for grouping speech feature vectors. It also uses **secure hashing techniques** to ensure safe handling and storage of user data.

---

## Features

-  **Speech-to-Text using Google API**
- **K-Means Clustering on Speech Vectors**
- **Secure Data Hashing (SHA-256)**
-  Clean and modular code structure

---

##  Tech Stack

| Component | Technology |
|----------|------------|
| Speech to Text | Google Cloud Speech-to-Text API |
| Clustering | K-Means (scikit-learn) |
| Security | SHA-256 Hashing |
| Backend | Python |
| Data Processing | NumPy, Pandas |

---

##  Project Structure

```
speech-to-text-clustering
├──  data
│   ├── create_sample_audio.py
│   └── sampke_audio.mp3
├──  src
│   ├── app.py
│   └── main.py
├── requirements.txt
└── README.md
```

---

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set Google API Credentials
```bash
export GOOGLE_APPLICATION_CREDENTIALS="your-key.json"
```

###  Run the project
```bash
python src/main.py
```

---

## Future Enhancements

- Speaker diarization
- Real-time clustering dashboard
- Deep learning embeddings (BERT / Wav2Vec2)
- Hosting using FastAPI + Docker

---

## License

MIT License

