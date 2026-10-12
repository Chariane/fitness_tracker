class Workout {
  const Workout({
    required this.id,
    required this.date,
    required this.type,
    required this.durationMinutes,
    required this.calories,
  });

  final String id;
  final String date;
  final String type;
  final int durationMinutes;
  final int calories;

  factory Workout.fromMap(String id, Map<String, dynamic> data) => Workout(
    id: id,
    date: data['date'] as String? ?? '',
    type: data['exerciseType'] as String? ?? 'Workout',
    durationMinutes: (data['durationMinutes'] as num?)?.toInt() ?? 0,
    calories: (data['caloriesBurned'] as num?)?.toInt() ?? 0,
  );

  Map<String, Object?> toMap() => {
    'date': date,
    'exerciseType': type,
    'durationMinutes': durationMinutes,
    'caloriesBurned': calories,
  };
}
