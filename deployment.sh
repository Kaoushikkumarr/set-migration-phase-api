# Below commands will be used for Deploying the code base to the Cloud Run Environment.

1. gcloud config set project m2m-wayfair-dev
2. gcloud builds submit --tag gcr.io/m2m-wayfair-dev/migration-phase:latest .
3. gcloud run deploy phases --image gcr.io/m2m-wayfair-dev/migration-phase:latest --platform managed --region us-central1 --allow-unauthenticated
4. Service URL: https://phases-b6a7nx5zsq-uc.a.run.app