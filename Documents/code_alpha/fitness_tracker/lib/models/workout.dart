class Workout {
  const Workout({
    required this.id,
    required this.date,
    required this.type,
    required this.durationMinutes,
    required this.calories,
    this.distanceKm,
    this.heartRateBpm,
    this.sets,
    this.repetitions,
    this.notes,
  });

  final String id;
  final String date;
  final String type;
  final int durationMinutes;
  final int calories;
  final double? distanceKm;
  final int? heartRateBpm;
  final int? sets;
  final int? repetitions;
  final String? notes;

  factory Workout.fromMap(String id, Map<String, dynamic> data) => Workout(
    id: id,
    date: data['date'] as String? ?? '',
    type: data['exerciseType'] as String? ?? 'Workout',
    durationMinutes: (data['durationMinutes'] as num?)?.toInt() ?? 0,
    calories: (data['caloriesBurned'] as num?)?.toInt() ?? 0,
    distanceKm: (data['distanceKm'] as num?)?.toDouble(),
    heartRateBpm: (data['heartRateBpm'] as num?)?.toInt(),
    sets: (data['sets'] as num?)?.toInt(),
    repetitions: (data['repetitions'] as num?)?.toInt(),
    notes: data['notes'] as String?,
  );

  Map<String, Object?> toMap() => {
    'date': date,
    'exerciseType': type,
    'durationMinutes': durationMinutes,
    'caloriesBurned': calories,
    'distanceKm': distanceKm,
    'heartRateBpm': heartRateBpm,
    'sets': sets,
    'repetitions': repetitions,
    'notes': notes,
  };
}
