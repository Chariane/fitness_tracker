# Pulse Fitness

Pulse Fitness is a Flutter fitness tracker for Chrome and Android. It lets you record daily steps and workouts, then review daily and weekly progress.

## Features

- Enter your daily step count
- Record an exercise type, duration, calories, and date
- View today’s activity and weekly step progress
- Review recent workouts
- Get clear validation messages when an entry is incomplete or invalid

## Run in Chrome

From the project folder, run:

    flutter pub get
    flutter run -d chrome --web-hostname=localhost --web-port=5000

The Firebase Web app configuration is included in `lib/services/fitness_service.dart`, so no `--dart-define` values are needed for Chrome. In VS Code, select **Pulse Fitness (Chrome, stable port)** in the Run and Debug menu and press F5. The fixed address (`http://localhost:5000`) lets Firebase reuse the same anonymous session across launches. Keep using this launch configuration; a different host or port creates a separate browser session.

## Firebase setup

This app uses Firebase Authentication and Cloud Firestore. In the Firebase project `fitness-tracker-efa37`:

1. Enable **Anonymous** under **Authentication → Sign-in method**.
2. If authentication returns `admin-restricted-operation`, open **Authentication → Settings → User actions** and allow account creation (sign-up).
3. Create a Cloud Firestore database.
4. Publish the rules from `firestore.rules`. They restrict each user to their own records.

The dashboard shows **Connecté** when Firebase is available. In preview mode, changes are temporary and are lost when the app closes.

## Android

The Flutter Android package is `com.example.fitness_tracker`. The Android app currently registered in Firebase was given the package `fitness.tracker`, so these do not match yet. Before testing Android with Firebase, register an Android app with package `com.example.fitness_tracker` or change the Flutter package to `fitness.tracker`. Provide the matching Firebase app ID when launching Android:

    flutter run --dart-define=FIREBASE_ANDROID_APP_ID=YOUR_ANDROID_APP_ID

The Android package registered in Firebase must match the app’s `applicationId` in `android/app/build.gradle.kts`.

## Database and backend

Cloud Firestore is the database and Firebase provides the hosted backend. The Flutter app accesses it through `lib/services/fitness_service.dart`; there is no separate server folder.

Records are stored under:

    users/{uid}/dailyStats/{date}
    users/{uid}/workouts/{workoutId}

Anonymous accounts are kept separately for each browser profile or app installation. Without a permanent sign-in method, records do not automatically sync between Chrome and Android.
