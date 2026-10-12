import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

import '../models/workout.dart';
import '../services/fitness_service.dart';

const ink = Color(0xFF1C2822);
const muted = Color(0xFF7A8980);
const line = Color(0xFFE8ECE7);
const canvas = Color(0xFFF5F6F2);
const green = Color(0xFF164E3B);
const lime = Color(0xFFB7E56A);

String _saveErrorMessage(Object error) {
  if (error is FirebaseException) {
    switch (error.code) {
      case 'permission-denied':
        return 'Firebase a refusé l’enregistrement. Vérifie les règles Firestore.';
      case 'unauthenticated':
        return 'La session a expiré. Relance l’application puis réessaie.';
      case 'unavailable':
      case 'deadline-exceeded':
        return 'Connexion à Firebase impossible. Vérifie Internet puis réessaie.';
      default:
        return 'Firebase n’a pas pu enregistrer les données : '
            '${error.message ?? error.code}';
    }
  }
  return 'L’enregistrement a échoué : $error';
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({required this.service, super.key});
  final FitnessService service;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  static const stepGoal = 10000;
  late final DateTime today;
  late final DateTime weekStart;
  late Stream<List<Workout>> workoutsStream;
  late Stream<Map<String, int>> stepsStream;

  @override
  void initState() {
    super.initState();
    today = FitnessService.startOfDay(DateTime.now());
    weekStart = FitnessService.startOfWeek(today);
    _createStreams();
  }

  @override
  void didUpdateWidget(covariant DashboardScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.service != widget.service) _createStreams();
  }

  void _createStreams() {
    final weekEnd = weekStart.add(const Duration(days: 6));
    workoutsStream = widget.service.watchWorkouts(weekStart, weekEnd);
    stepsStream = widget.service.watchSteps(weekStart, weekEnd);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 76,
        titleSpacing: 22,
        title: Row(
          children: [
            Container(
              width: 38,
              height: 38,
              decoration: BoxDecoration(
                color: green,
                borderRadius: BorderRadius.circular(13),
              ),
              child: const Icon(Icons.bolt_rounded, color: lime, size: 24),
            ),
            const SizedBox(width: 11),
            const Text(
              'pulse',
              style: TextStyle(
                fontSize: 23,
                fontWeight: FontWeight.w800,
                letterSpacing: -1.1,
              ),
            ),
          ],
        ),
        actions: [
          Container(
            margin: const EdgeInsets.only(right: 22),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: widget.service.isConnected
                  ? const Color(0xFFE7F3EA)
                  : const Color(0xFFFFF2D9),
              borderRadius: BorderRadius.circular(30),
            ),
            child: Row(
              children: [
                Icon(
                  widget.service.isConnected
                      ? Icons.cloud_done_outlined
                      : Icons.visibility_outlined,
                  size: 15,
                  color: widget.service.isConnected
                      ? green
                      : const Color(0xFF9A6A10),
                ),
                const SizedBox(width: 6),
                Text(
                  widget.service.isConnected ? 'Connecté' : 'Aperçu',
                  style: TextStyle(
                    fontSize: 11,
                    fontWeight: FontWeight.w700,
                    color: widget.service.isConnected
                        ? green
                        : const Color(0xFF9A6A10),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
      body: StreamBuilder<List<Workout>>(
        stream: workoutsStream,
        builder: (context, workoutSnapshot) {
          final workouts = workoutSnapshot.data ?? const <Workout>[];
          return StreamBuilder<Map<String, int>>(
            stream: stepsStream,
            builder: (context, stepSnapshot) {
              final steps = stepSnapshot.data ?? const <String, int>{};
              final wide = MediaQuery.sizeOf(context).width >= 780;
              return Center(
                child: ConstrainedBox(
                  constraints: const BoxConstraints(maxWidth: 1120),
                  child: SingleChildScrollView(
                    padding: EdgeInsets.fromLTRB(
                      wide ? 36 : 20,
                      20,
                      wide ? 36 : 20,
                      36,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        _pageHeading(),
                        const SizedBox(height: 25),
                        _topCards(
                          context,
                          wide: wide,
                          steps: steps[FitnessService.dateKey(today)] ?? 0,
                          workouts: workouts,
                        ),
                        const SizedBox(height: 25),
                        wide
                            ? Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Expanded(flex: 6, child: _weeklyCard(steps)),
                                  const SizedBox(width: 20),
                                  Expanded(
                                    flex: 4,
                                    child: _activityCard(workouts),
                                  ),
                                ],
                              )
                            : Column(
                                children: [
                                  _weeklyCard(steps),
                                  const SizedBox(height: 18),
                                  _activityCard(workouts),
                                ],
                              ),
                        if (!widget.service.isConnected) ...[
                          const SizedBox(height: 18),
                          _demoNotice(),
                        ],
                      ],
                    ),
                  ),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _showWorkoutForm(context),
        backgroundColor: green,
        foregroundColor: Colors.white,
        icon: const Icon(Icons.add_rounded),
        label: const Text(
          'Ajouter une séance',
          style: TextStyle(fontWeight: FontWeight.w700),
        ),
      ),
    );
  }

  Widget _pageHeading() {
    final now = DateTime.now();
    const months = [
      'janvier',
      'février',
      'mars',
      'avril',
      'mai',
      'juin',
      'juillet',
      'août',
      'septembre',
      'octobre',
      'novembre',
      'décembre',
    ];
    const weekdays = [
      'lundi',
      'mardi',
      'mercredi',
      'jeudi',
      'vendredi',
      'samedi',
      'dimanche',
    ];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          weekdays[now.weekday - 1] +
              ' ' +
              now.day.toString() +
              ' ' +
              months[now.month - 1],
          style: const TextStyle(
            color: muted,
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 7),
        const Text(
          'Bonjour, Nadège 👋',
          style: TextStyle(
            color: ink,
            fontSize: 29,
            fontWeight: FontWeight.w800,
            letterSpacing: -1.1,
          ),
        ),
        const SizedBox(height: 5),
        const Text(
          'Chaque mouvement compte. Voici ton activité.',
          style: TextStyle(color: muted, fontSize: 14),
        ),
      ],
    );
  }

  Widget _topCards(
    BuildContext context, {
    required bool wide,
    required int steps,
    required List<Workout> workouts,
  }) {
    final todaysWorkouts = workouts
        .where((w) => w.date == FitnessService.dateKey(today))
        .toList();
    final minutes = todaysWorkouts.fold<int>(
      0,
      (sum, workout) => sum + workout.durationMinutes,
    );
    final calories = todaysWorkouts.fold<int>(
      0,
      (sum, workout) => sum + workout.calories,
    );
    final stepCard = _stepsCard(context, steps);

    Widget caloriesCard() => _metricCard(
      icon: Icons.local_fire_department_outlined,
      label: 'Calories brûlées',
      value: calories.toString(),
      unit: 'kcal',
      tint: const Color(0xFFFFEEE8),
      iconColor: const Color(0xFFE68156),
    );

    Widget timeCard() => _metricCard(
      icon: Icons.timer_outlined,
      label: 'Temps actif',
      value: minutes.toString(),
      unit: 'min',
      tint: const Color(0xFFE9F0FF),
      iconColor: const Color(0xFF597CCB),
    );

    if (wide) {
      return SizedBox(
        height: 202,
        child: Row(
          children: [
            Expanded(flex: 11, child: stepCard),
            const SizedBox(width: 16),
            Expanded(
              flex: 9,
              child: Column(
                children: [
                  Expanded(child: caloriesCard()),
                  const SizedBox(height: 12),
                  Expanded(child: timeCard()),
                ],
              ),
            ),
          ],
        ),
      );
    }

    return Column(
      children: [
        SizedBox(height: 205, child: stepCard),
        const SizedBox(height: 14),
        SizedBox(
          height: 112,
          child: Row(
            children: [
              Expanded(child: caloriesCard()),
              const SizedBox(width: 14),
              Expanded(child: timeCard()),
            ],
          ),
        ),
      ],
    );
  }

  Widget _stepsCard(BuildContext context, int steps) => Container(
    padding: const EdgeInsets.all(22),
    decoration: BoxDecoration(
      color: green,
      borderRadius: BorderRadius.circular(25),
    ),
    child: Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Row(
                children: [
                  const Icon(Icons.directions_walk, color: lime, size: 19),
                  const SizedBox(width: 7),
                  const Text(
                    'Pas aujourd’hui',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 13,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    tooltip: 'Saisir le nombre de pas',
                    onPressed: () => _showStepsDialog(context, steps),
                    visualDensity: VisualDensity.compact,
                    icon: const Icon(
                      Icons.edit_outlined,
                      color: Colors.white70,
                      size: 18,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 7),
              Text(
                _number(steps),
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 38,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -1.5,
                ),
              ),
              const SizedBox(height: 6),
              Text(
                _number(stepGoal) + ' pas par jour',
                style: const TextStyle(color: Colors.white60, fontSize: 12),
              ),
            ],
          ),
        ),
        const SizedBox(width: 15),
        SizedBox(
          width: 106,
          height: 106,
          child: Stack(
            alignment: Alignment.center,
            children: [
              SizedBox.expand(
                child: CircularProgressIndicator(
                  value: (steps / stepGoal).clamp(0.0, 1.0),
                  strokeWidth: 9,
                  backgroundColor: Colors.white.withValues(alpha: .16),
                  valueColor: const AlwaysStoppedAnimation(lime),
                  strokeCap: StrokeCap.round,
                ),
              ),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    ((steps / stepGoal) * 100).round().toString() + '%',
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w800,
                      fontSize: 21,
                    ),
                  ),
                  const Text(
                    'objectif',
                    style: TextStyle(color: Colors.white60, fontSize: 10),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    ),
  );

  Widget _metricCard({
    required IconData icon,
    required String label,
    required String value,
    required String unit,
    required Color tint,
    required Color iconColor,
  }) => Container(
    width: double.infinity,
    padding: const EdgeInsets.all(17),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(22),
      border: Border.all(color: line),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            Container(
              width: 34,
              height: 34,
              decoration: BoxDecoration(
                color: tint,
                borderRadius: BorderRadius.circular(11),
              ),
              child: Icon(icon, size: 18, color: iconColor),
            ),
            const SizedBox(width: 9),
            Flexible(
              child: Text(
                label,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: muted,
                  fontSize: 11,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ),
          ],
        ),
        Row(
          crossAxisAlignment: CrossAxisAlignment.end,
          children: [
            Text(
              value,
              style: const TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.w800,
                color: ink,
                letterSpacing: -1,
              ),
            ),
            const SizedBox(width: 6),
            Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(
                unit,
                style: const TextStyle(color: muted, fontSize: 11),
              ),
            ),
          ],
        ),
      ],
    ),
  );

  Widget _weeklyCard(Map<String, int> steps) {
    final days = List.generate(
      7,
      (index) => weekStart.add(Duration(days: index)),
    );
    final values = days
        .map((day) => steps[FitnessService.dateKey(day)] ?? 0)
        .toList();
    final total = values.fold<int>(0, (sum, value) => sum + value);
    const labels = ['L', 'M', 'M', 'J', 'V', 'S', 'D'];

    return _panel(
      title: 'Cette semaine',
      trailing: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: const Color(0xFFF1F4EF),
          borderRadius: BorderRadius.circular(20),
        ),
        child: const Text(
          'Semaine en cours',
          style: TextStyle(
            color: muted,
            fontSize: 10,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            _number(total),
            style: const TextStyle(
              fontSize: 28,
              color: ink,
              fontWeight: FontWeight.w800,
              letterSpacing: -1,
            ),
          ),
          const Text(
            'pas au total',
            style: TextStyle(color: muted, fontSize: 11),
          ),
          const SizedBox(height: 22),
          SizedBox(
            height: 126,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: List.generate(7, (index) {
                final active =
                    days[index].weekday == DateTime.now().weekday &&
                    FitnessService.dateKey(days[index]) ==
                        FitnessService.dateKey(DateTime.now());
                final ratio = (values[index] / 10000).clamp(0.05, 1.0);
                return Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 5),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        Text(
                          values[index] == 0 ? '' : _compact(values[index]),
                          style: const TextStyle(
                            color: muted,
                            fontSize: 9,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                        const SizedBox(height: 7),
                        Expanded(
                          child: Align(
                            alignment: Alignment.bottomCenter,
                            child: FractionallySizedBox(
                              heightFactor: values[index] == 0 ? 0.04 : ratio,
                              widthFactor: .72,
                              child: DecoratedBox(
                                decoration: BoxDecoration(
                                  color: active
                                      ? green
                                      : const Color(0xFFDCE9D5),
                                  borderRadius: BorderRadius.circular(9),
                                ),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 9),
                        Text(
                          labels[index],
                          style: TextStyle(
                            color: active ? green : muted,
                            fontSize: 10,
                            fontWeight: active
                                ? FontWeight.w800
                                : FontWeight.w500,
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }),
            ),
          ),
        ],
      ),
    );
  }

  Widget _activityCard(List<Workout> workouts) {
    final visible = workouts.take(4).toList();

    return _panel(
      title: 'Séances récentes',
      trailing: Text(
        workouts.length.toString() + ' cette semaine',
        style: const TextStyle(
          color: muted,
          fontSize: 11,
          fontWeight: FontWeight.w600,
        ),
      ),
      child: visible.isEmpty
          ? const Padding(
              padding: EdgeInsets.symmetric(vertical: 24),
              child: Center(
                child: Text(
                  'Pas encore de séance cette semaine.',
                  style: TextStyle(color: muted, fontSize: 12),
                ),
              ),
            )
          : Column(
              children: [
                for (var i = 0; i < visible.length; i++) ...[
                  _workoutRow(visible[i]),
                  if (i != visible.length - 1)
                    const Divider(height: 18, color: line),
                ],
              ],
            ),
    );
  }

  Widget _workoutRow(Workout workout) {
    final icon =
        workout.type.toLowerCase().contains('run') ||
            workout.type.toLowerCase().contains('course')
        ? Icons.directions_run_rounded
        : workout.type.toLowerCase().contains('cycl')
        ? Icons.directions_bike_rounded
        : workout.type.toLowerCase().contains('walk') ||
              workout.type.toLowerCase().contains('marche')
        ? Icons.directions_walk_rounded
        : Icons.fitness_center_rounded;
    return Row(
      children: [
        Container(
          width: 41,
          height: 41,
          decoration: BoxDecoration(
            color: const Color(0xFFF0F4ED),
            borderRadius: BorderRadius.circular(13),
          ),
          child: Icon(icon, color: green, size: 20),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                workout.type,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: ink,
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                workout.durationMinutes.toString() +
                    ' min  ·  ' +
                    workout.calories.toString() +
                    ' kcal',
                style: const TextStyle(color: muted, fontSize: 10),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _panel({
    required String title,
    required Widget trailing,
    required Widget child,
  }) => Container(
    width: double.infinity,
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(
      color: Colors.white,
      border: Border.all(color: line),
      borderRadius: BorderRadius.circular(23),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                title,
                style: const TextStyle(
                  color: ink,
                  fontSize: 15,
                  fontWeight: FontWeight.w800,
                ),
              ),
            ),
            trailing,
          ],
        ),
        const SizedBox(height: 19),
        child,
      ],
    ),
  );

  Widget _demoNotice() => Container(
    width: double.infinity,
    padding: const EdgeInsets.all(14),
    decoration: BoxDecoration(
      color: const Color(0xFFFFF7E8),
      borderRadius: BorderRadius.circular(15),
      border: Border.all(color: const Color(0xFFF2E4C8)),
    ),
    child: Row(
      children: [
        const Icon(Icons.info_outline, color: Color(0xFF9A6A10), size: 18),
        const SizedBox(width: 10),
        Expanded(
          child: Text(
            widget.service.connectionError ??
                'Mode aperçu : les modifications ne sont pas enregistrées. Configure Firebase pour activer la sauvegarde.',
            style: const TextStyle(
              color: Color(0xFF7A5A20),
              fontSize: 11,
              height: 1.4,
            ),
          ),
        ),
      ],
    ),
  );

  Future<void> _showStepsDialog(BuildContext context, int current) async {
    final value = await showDialog<int>(
      context: context,
      builder: (_) => StepsDialog(current: current),
    );
    if (value == null || !mounted) return;

    try {
      await widget.service.setTodaySteps(value);
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        this.context,
      ).showSnackBar(SnackBar(content: Text(_saveErrorMessage(error))));
    }
  }

  Future<void> _showWorkoutForm(BuildContext context) async {
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => WorkoutFormSheet(service: widget.service),
    );
  }

  String _number(int value) {
    final raw = value.toString();
    final out = StringBuffer();
    for (var i = 0; i < raw.length; i++) {
      if (i > 0 && (raw.length - i) % 3 == 0) out.write(' ');
      out.write(raw[i]);
    }
    return out.toString();
  }

  String _compact(int value) => value >= 1000
      ? (value / 1000).toStringAsFixed(1) + 'k'
      : value.toString();
}

class StepsDialog extends StatefulWidget {
  const StepsDialog({required this.current, super.key});

  final int current;

  @override
  State<StepsDialog> createState() => _StepsDialogState();
}

class _StepsDialogState extends State<StepsDialog> {
  final formKey = GlobalKey<FormState>();
  late final TextEditingController controller;

  @override
  void initState() {
    super.initState();
    controller = TextEditingController(text: widget.current.toString());
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) => AlertDialog(
    title: const Text('Saisir tes pas'),
    content: Form(
      key: formKey,
      child: TextFormField(
        controller: controller,
        autofocus: true,
        keyboardType: TextInputType.number,
        decoration: const InputDecoration(
          labelText: 'Nombre de pas aujourd’hui',
          suffixText: 'pas',
          errorMaxLines: 2,
        ),
        validator: (text) {
          final value = text?.trim() ?? '';
          if (value.isEmpty) return 'Saisis ton nombre de pas.';
          final number = int.tryParse(value);
          if (number == null) {
            return 'Entre un nombre entier, sans virgule (ex. 7500).';
          }
          if (number < 0) return 'Le nombre de pas ne peut pas être négatif.';
          return null;
        },
      ),
    ),
    actions: [
      TextButton(
        onPressed: () => Navigator.pop(context),
        child: const Text('Annuler'),
      ),
      FilledButton(
        onPressed: () {
          if (formKey.currentState!.validate()) {
            Navigator.pop(context, int.parse(controller.text.trim()));
          }
        },
        child: const Text('Enregistrer'),
      ),
    ],
  );
}

class WorkoutFormSheet extends StatefulWidget {
  const WorkoutFormSheet({required this.service, super.key});
  final FitnessService service;

  @override
  State<WorkoutFormSheet> createState() => _WorkoutFormSheetState();
}

class _WorkoutFormSheetState extends State<WorkoutFormSheet> {
  final formKey = GlobalKey<FormState>();
  final durationController = TextEditingController();
  final caloriesController = TextEditingController();
  String exercise = 'Course';
  DateTime date = DateTime.now();
  bool saving = false;

  static const exercises = [
    'Course',
    'Marche',
    'Vélo',
    'Musculation',
    'Yoga',
    'Autre',
  ];

  @override
  void dispose() {
    durationController.dispose();
    caloriesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final bottomInset = MediaQuery.viewInsetsOf(context).bottom;
    return Container(
      padding: EdgeInsets.fromLTRB(22, 12, 22, 22 + bottomInset),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(26)),
      ),
      child: SingleChildScrollView(
        child: Form(
          key: formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Center(
                child: Container(
                  width: 40,
                  height: 4,
                  decoration: BoxDecoration(
                    color: line,
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ),
              const SizedBox(height: 22),
              const Text(
                'Nouvelle séance',
                style: TextStyle(
                  color: ink,
                  fontSize: 22,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -.5,
                ),
              ),
              const SizedBox(height: 5),
              const Text(
                'Ajoute les détails de ton activité.',
                style: TextStyle(color: muted, fontSize: 13),
              ),
              const SizedBox(height: 22),
              DropdownButtonFormField<String>(
                value: exercise,
                decoration: const InputDecoration(
                  labelText: 'Type d’exercice',
                  border: OutlineInputBorder(),
                ),
                items: exercises
                    .map(
                      (name) =>
                          DropdownMenuItem(value: name, child: Text(name)),
                    )
                    .toList(),
                onChanged: (value) {
                  if (value != null) setState(() => exercise = value);
                },
              ),
              const SizedBox(height: 14),
              Row(
                children: [
                  Expanded(
                    child: TextFormField(
                      controller: durationController,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Durée',
                        suffixText: 'min',
                        border: OutlineInputBorder(),
                        errorMaxLines: 2,
                      ),
                      validator: (value) => _positiveInteger(value, 'durée'),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: TextFormField(
                      controller: caloriesController,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Calories',
                        suffixText: 'kcal',
                        border: OutlineInputBorder(),
                        errorMaxLines: 2,
                      ),
                      validator: (value) => _positiveInteger(value, 'calories'),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 14),
              OutlinedButton.icon(
                onPressed: _pickDate,
                icon: const Icon(Icons.calendar_today_outlined, size: 17),
                label: Text(
                  date.year == DateTime.now().year &&
                          date.month == DateTime.now().month &&
                          date.day == DateTime.now().day
                      ? 'Aujourd’hui'
                      : date.day.toString() +
                            '/' +
                            date.month.toString() +
                            '/' +
                            date.year.toString(),
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                height: 50,
                child: FilledButton.icon(
                  onPressed: saving ? null : _save,
                  icon: saving
                      ? const SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: Colors.white,
                          ),
                        )
                      : const Icon(Icons.check_rounded),
                  label: Text(
                    saving ? 'Enregistrement…' : 'Enregistrer la séance',
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String? _positiveInteger(String? value, String field) {
    final text = value?.trim() ?? '';
    final isDuration = field == 'durée';
    if (text.isEmpty) {
      return isDuration
          ? 'Saisis la durée de la séance.'
          : 'Saisis les calories brûlées.';
    }

    final parsed = int.tryParse(text);
    if (parsed == null) {
      return isDuration
          ? 'Entre une durée en minutes, sans virgule (ex. 30).'
          : 'Entre les calories en nombre entier, sans virgule (ex. 250).';
    }
    if (parsed < 0) {
      return isDuration
          ? 'La durée ne peut pas être négative.'
          : 'Les calories ne peuvent pas être négatives.';
    }
    if (isDuration && parsed == 0) {
      return 'La durée doit être d’au moins 1 minute.';
    }
    return null;
  }

  Future<void> _pickDate() async {
    final selected = await showDatePicker(
      context: context,
      initialDate: date,
      firstDate: DateTime.now().subtract(const Duration(days: 365)),
      lastDate: DateTime.now(),
      locale: const Locale('fr'),
    );
    if (!mounted || selected == null) return;
    setState(() => date = selected);
  }

  Future<void> _save() async {
    if (!formKey.currentState!.validate()) return;
    setState(() => saving = true);
    try {
      await widget.service.addWorkout(
        type: exercise,
        duration: int.parse(durationController.text.trim()),
        calories: int.parse(caloriesController.text.trim()),
        date: date,
      );
      if (mounted) Navigator.pop(context);
    } catch (error) {
      if (!mounted) return;
      setState(() => saving = false);
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(_saveErrorMessage(error))));
    }
  }
}
