# Pulse Fitness

Pulse Fitness is a Flutter fitness tracker for Chrome and Android. It lets you record daily steps and workouts, then review daily and weekly progress.

The interface includes light and dark themes, a custom Pulse logo, and subtle animations for the dashboard, progress ring, step count, and weekly chart.

## Features

- Switch between light and dark themes; the selected theme is saved on the device
- Enter your daily step count
- Record an exercise type, duration, calories, and date, with optional distance, heart rate, strength sets/repetitions, and notes
- Select any day in a week and inspect its steps and workouts
- Browse previous weeks and compare weekly steps, sessions, active minutes, and calories
- Edit or delete a workout entry; summaries show the extra details entered
- Get clear validation messages when an entry is incomplete or invalid
- See the Pulse logo in the browser tab and when installing the web app
- Personalize the dashboard greeting with a name saved to the Firebase Authentication profile

## Run in Chrome

From the project folder, run:

    flutter pub get
    flutter run -d web-server --web-hostname=localhost --web-port=5000

Open the URL printed by Flutter in your regular Chrome browser. Use this same address for each launch so Firebase keeps using the same anonymous account. The Firebase Web app configuration is included in `lib/services/fitness_service.dart`, so no `--dart-define` values are needed for Chrome. In VS Code, select **Pulse Fitness Web (persistent Chrome session)**, start the server, then open its URL in Chrome.

## Firebase setup

This app uses Firebase Authentication and Cloud Firestore. In the Firebase project `fitness-tracker-efa37`:

1. Enable **Anonymous** under **Authentication → Sign-in method**.
2. If authentication returns `admin-restricted-operation`, open **Authentication → Settings → User actions** and allow account creation (sign-up).
3. Create a Cloud Firestore database.
4. Publish the rules from `firestore.rules`. They restrict each user to their own records.

The dashboard shows **Connecté** when Firebase is available. In preview mode, changes are temporary and are lost when the app closes.

On the first connected launch, Pulse asks what name to use in the greeting. You can change it later with the edit icon beside the greeting. The name is stored in the Firebase Authentication profile for that anonymous account.

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
