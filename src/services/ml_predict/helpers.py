import boto3
import pickle
import warnings
from decouple import config

def get_comment_select_query():
        return '''
            SELECT id, body
            FROM Reddit.Comment
            WHERE id NOT IN (SELECT idcomment FROM Reddit.Sentiment)
            ORDER BY id
        '''

def get_sentiment_insert_query():
        return '''
        INSERT INTO Reddit.Sentiment (
            idComment,
            score
        )
        VALUES (
            %(id)s,
            %(score)s
        )
        -- Dont insert duplicates
        ON CONFLICT (idComment) DO NOTHING; 
        '''

def load_artifacts_from_s3():
    s3 = boto3.client('s3', region_name=config('AWS_DEFAULT_REGION'),
                            aws_access_key_id=config('AWS_ACCESS_KEY_ID'), 
                            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                            aws_session_token=config('AWS_SESSION_TOKEN'))

    BUCKET = config('AWS_S3_ML_ARTIFACTS_BUCKET')

    print("importing model, vectorizer and pca estimators...")

    # Filter incoming warnings when importing model, vectorizer and pca estimators 
    warnings.filterwarnings(action="ignore", message="Trying to unpickle estimator")
    model = pickle.loads(s3.get_object(Bucket=BUCKET, Key="sentiment_svm_model.pkl")['Body'].read())
    vectorizer = pickle.loads(s3.get_object(Bucket=BUCKET, Key="Tfidf_Vectorizer_v1.pkl")['Body'].read())
    pca = pickle.loads(s3.get_object(Bucket=BUCKET, Key="pca_v1.pkl")['Body'].read())

    return model, vectorizer, pca