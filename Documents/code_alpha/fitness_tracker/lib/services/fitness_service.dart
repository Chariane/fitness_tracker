import 'dart:async';

import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

import '../models/workout.dart';

class FitnessService {
  FitnessService._({
    FirebaseFirestore? firestore,
    String? userId,
    this.connectionError,
  }) : _firestore = firestore,
       _userId = userId;

  final FirebaseFirestore? _firestore;
  final String? _userId;
  final String? connectionError;
  bool get isConnected => _firestore != null;

  final List<Workout> _demoWorkouts = [
    Workout(
      id: 'demo-1',
      date: dateKey(DateTime.now()),
      type: 'Morning run',
      durationMinutes: 32,
      calories: 248,
    ),
    Workout(
      id: 'demo-2',
      date: dateKey(DateTime.now().subtract(const Duration(days: 1))),
      type: 'Strength training',
      durationMinutes: 45,
      calories: 310,
    ),
    Workout(
      id: 'demo-3',
      date: dateKey(DateTime.now().subtract(const Duration(days: 3))),
      type: 'Cycling',
      durationMinutes: 28,
      calories: 190,
    ),
  ];

  final Map<String, int> _demoSteps = {
    dateKey(DateTime.now()): 6842,
    dateKey(DateTime.now().subtract(const Duration(days: 1))): 8420,
    dateKey(DateTime.now().subtract(const Duration(days: 2))): 5310,
    dateKey(DateTime.now().subtract(const Duration(days: 3))): 9730,
    dateKey(DateTime.now().subtract(const Duration(days: 4))): 6240,
    dateKey(DateTime.now().subtract(const Duration(days: 5))): 7800,
    dateKey(DateTime.now().subtract(const Duration(days: 6))): 4560,
  };

  final StreamController<void> _changes = StreamController<void>.broadcast();

  static String define(String name) {
    switch (name) {
      case 'FIREBASE_API_KEY':
        return const String.fromEnvironment(
          'FIREBASE_API_KEY',
          defaultValue: 'AIzaSyDxuYAUAh7ZmC8M0oKgzJAJavAbxw2f1XM',
        );
      case 'FIREBASE_SENDER_ID':
        return const String.fromEnvironment(
          'FIREBASE_SENDER_ID',
          defaultValue: '1080237765112',
        );
      case 'FIREBASE_WEB_APP_ID':
        return const String.fromEnvironment(
          'FIREBASE_WEB_APP_ID',
          defaultValue: '1:1080237765112:web:ec245a25fb163c5371660d',
        );
      case 'FIREBASE_ANDROID_APP_ID':
        return const String.fromEnvironment('FIREBASE_ANDROID_APP_ID');
      case 'FIREBASE_AUTH_DOMAIN':
        return const String.fromEnvironment(
          'FIREBASE_AUTH_DOMAIN',
          defaultValue: 'fitness-tracker-efa37.firebaseapp.com',
        );
      default:
        return '';
    }
  }

  factory FitnessService.preview() => FitnessService._();

  static Future<FitnessService> connect() async {
    const projectId = 'fitness-tracker-efa37';
    final apiKey = define('FIREBASE_API_KEY');
    final senderId = define('FIREBASE_SENDER_ID');
    final appId = kIsWeb
        ? define('FIREBASE_WEB_APP_ID')
        : define('FIREBASE_ANDROID_APP_ID');

    if (apiKey.isEmpty || senderId.isEmpty || appId.isEmpty) {
      return FitnessService._(
        connectionError: 'Les paramètres Firebase sont incomplets.',
      );
    }

    try {
      if (Firebase.apps.isEmpty) {
        await Firebase.initializeApp(
          options: FirebaseOptions(
            apiKey: apiKey,
            appId: appId,
            messagingSenderId: senderId,
            projectId: projectId,
            authDomain: define('FIREBASE_AUTH_DOMAIN'),
          ),
        );
      }
      final auth = FirebaseAuth.instance;
      final existingUser = await auth.authStateChanges().first;
      final user = existingUser ?? (await auth.signInAnonymously()).user;
      final uid = user?.uid;
      if (uid != null) {
        return FitnessService._(
          firestore: FirebaseFirestore.instance,
          userId: uid,
        );
      }
    } catch (error) {
      debugPrint('Firebase setup is not ready: $error');
      return FitnessService._(connectionError: error.toString());
    }
    return FitnessService._(
      connectionError: 'Firebase Authentication n’a pas retourné de compte.',
    );
  }

  CollectionReference<Map<String, dynamic>> get _workouts =>
      _firestore!.collection('users').doc(_userId).collection('workouts');

  CollectionReference<Map<String, dynamic>> get _dailyStats =>
      _firestore!.collection('users').doc(_userId).collection('dailyStats');

  Stream<List<Workout>> watchWorkouts(DateTime from, DateTime to) {
    if (_firestore != null) {
      return _workouts
          .where('date', isGreaterThanOrEqualTo: dateKey(from))
          .where('date', isLessThanOrEqualTo: dateKey(to))
          .snapshots()
          .map((snapshot) {
            final items =
                snapshot.docs
                    .map((doc) => Workout.fromMap(doc.id, doc.data()))
                    .toList()
                  ..sort((a, b) => b.date.compareTo(a.date));
            return items;
          });
    }
    return _demoWatch(
      () =>
          _demoWorkouts
              .where(
                (w) =>
                    w.date.compareTo(dateKey(from)) >= 0 &&
                    w.date.compareTo(dateKey(to)) <= 0,
              )
              .toList()
            ..sort((a, b) => b.date.compareTo(a.date)),
    );
  }

  Stream<Map<String, int>> watchSteps(DateTime from, DateTime to) {
    if (_firestore != null) {
      return _dailyStats
          .where('date', isGreaterThanOrEqualTo: dateKey(from))
          .where('date', isLessThanOrEqualTo: dateKey(to))
          .snapshots()
          .map(
            (snapshot) => {
              for (final doc in snapshot.docs)
                doc.data()['date'] as String:
                    (doc.data()['steps'] as num?)?.toInt() ?? 0,
            },
          );
    }
    return _demoWatch(() => Map<String, int>.from(_demoSteps));
  }

  Stream<T> _demoWatch<T>(T Function() read) async* {
    yield read();
    await for (final _ in _changes.stream) {
      yield read();
    }
  }

  Future<void> addWorkout({
    required String type,
    required int duration,
    required int calories,
    required DateTime date,
  }) async {
    final key = dateKey(date);
    if (_firestore != null) {
      await _workouts.add({
        'date': key,
        'exerciseType': type,
        'durationMinutes': duration,
        'caloriesBurned': calories,
        'createdAt': FieldValue.serverTimestamp(),
      });
    } else {
      _demoWorkouts.insert(
        0,
        Workout(
          id: 'demo-' + DateTime.now().microsecondsSinceEpoch.toString(),
          date: key,
          type: type,
          durationMinutes: duration,
          calories: calories,
        ),
      );
      _changes.add(null);
    }
  }

  Future<void> setTodaySteps(int steps) async {
    final key = dateKey(DateTime.now());
    if (_firestore != null) {
      await _dailyStats.doc(key).set({
        'date': key,
        'steps': steps,
        'updatedAt': FieldValue.serverTimestamp(),
      }, SetOptions(merge: true));
    } else {
      _demoSteps[key] = steps;
      _changes.add(null);
    }
  }

  static String dateKey(DateTime date) =>
      date.toIso8601String().substring(0, 10);

  static DateTime startOfDay(DateTime date) =>
      DateTime(date.year, date.month, date.day);

  static DateTime startOfWeek(DateTime date) =>
      startOfDay(date).subtract(Duration(days: date.weekday - 1));

  static int dayOfWeek(String date) {
    final parts = date.split('-').map(int.parse).toList();
    return DateTime(parts[0], parts[1], parts[2]).weekday - 1;
  }
}
