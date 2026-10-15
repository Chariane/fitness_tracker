import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

import '../models/workout.dart';
import '../services/fitness_service.dart';

const green = Color(0xFF164E3B);
const lime = Color(0xFFB7E56A);

Color _ink(BuildContext context) => Theme.of(context).colorScheme.onSurface;
Color _muted(BuildContext context) =>
    Theme.of(context).colorScheme.onSurfaceVariant;
Color _line(BuildContext context) =>
    Theme.of(context).colorScheme.outlineVariant;
Color _panelSurface(BuildContext context) =>
    Theme.of(context).colorScheme.surfaceContainerLow;
Color _softSurface(BuildContext context) =>
    Theme.of(context).colorScheme.surfaceContainer;

class _PulseLogo extends StatelessWidget {
  const _PulseLogo({required this.size});

  final double size;

  @override
  Widget build(BuildContext context) => Container(
    width: size,
    height: size,
    decoration: BoxDecoration(
      gradient: const LinearGradient(
        colors: [Color(0xFF10392C), Color(0xFF267253)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
      borderRadius: BorderRadius.circular(size * .32),
      boxShadow: [
        BoxShadow(
          color: green.withValues(alpha: .2),
          blurRadius: 12,
          offset: const Offset(0, 5),
        ),
      ],
    ),
    child: Icon(Icons.monitor_heart_rounded, color: lime, size: size * .64),
  );
}

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

String _shortDate(DateTime date) {
  const months = [
    'janv.',
    'févr.',
    'mars',
    'avr.',
    'mai',
    'juin',
    'juil.',
    'août',
    'sept.',
    'oct.',
    'nov.',
    'déc.',
  ];
  return '${date.day} ${months[date.month - 1]}';
}

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({
    required this.service,
    required this.isDark,
    required this.onThemeToggle,
    super.key,
  });
  final FitnessService service;
  final bool isDark;
  final VoidCallback onThemeToggle;

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen>
    with SingleTickerProviderStateMixin {
  static const stepGoal = 10000;
  late final DateTime today;
  late DateTime weekStart;
  late DateTime selectedDay;
  late Stream<List<Workout>> workoutsStream;
  late Stream<Map<String, int>> stepsStream;
  late final AnimationController introController;
  String? userName;

  @override
  void initState() {
    super.initState();
    introController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 900),
    )..forward();
    today = FitnessService.startOfDay(DateTime.now());
    weekStart = FitnessService.startOfWeek(today);
    selectedDay = today;
    userName = widget.service.userName;
    _createStreams();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted &&
          widget.service.isConnected &&
          (userName?.isEmpty ?? true)) {
        _editName();
      }
    });
  }

  @override
  void dispose() {
    introController.dispose();
    super.dispose();
  }

  Widget _entrance(Widget child, double start) {
    final animation = CurvedAnimation(
      parent: introController,
      curve: Interval(start, 1, curve: Curves.easeOutCubic),
    );
    return FadeTransition(
      opacity: animation,
      child: SlideTransition(
        position: Tween<Offset>(
          begin: const Offset(0, .055),
          end: Offset.zero,
        ).animate(animation),
        child: child,
      ),
    );
  }

  @override
  void didUpdateWidget(covariant DashboardScreen oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.service != widget.service) {
      userName = widget.service.userName;
      _createStreams();
    }
  }

  void _createStreams() {
    final weekEnd = weekStart.add(const Duration(days: 6));
    workoutsStream = widget.service.watchWorkouts(weekStart, weekEnd);
    stepsStream = widget.service.watchSteps(weekStart, weekEnd);
  }

  void _changeWeek(int offset) {
    final nextWeek = weekStart.add(Duration(days: offset * 7));
    final currentWeek = FitnessService.startOfWeek(today);
    final earliestWeek = FitnessService.startOfWeek(
      today.subtract(const Duration(days: 365)),
    );
    if (nextWeek.isBefore(earliestWeek) || nextWeek.isAfter(currentWeek)) {
      return;
    }

    final weekdayOffset = selectedDay.weekday - 1;
    setState(() {
      weekStart = nextWeek;
      selectedDay = nextWeek.add(Duration(days: weekdayOffset));
      _createStreams();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 76,
        titleSpacing: 22,
        title: Row(
          children: [
            _PulseLogo(size: 38),
            const SizedBox(width: 11),
            Text(
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
          IconButton(
            tooltip: widget.isDark
                ? 'Activer le mode clair'
                : 'Activer le mode sombre',
            onPressed: widget.onThemeToggle,
            icon: Icon(
              widget.isDark
                  ? Icons.light_mode_rounded
                  : Icons.dark_mode_rounded,
            ),
          ),
          Container(
            margin: const EdgeInsets.only(right: 22),
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            decoration: BoxDecoration(
              color: widget.service.isConnected
                  ? (widget.isDark
                        ? const Color(0xFF20392D)
                        : const Color(0xFFE7F3EA))
                  : (widget.isDark
                        ? const Color(0xFF3D3220)
                        : const Color(0xFFFFF2D9)),
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
                        _entrance(_pageHeading(), 0),
                        const SizedBox(height: 25),
                        _entrance(
                          _topCards(
                            context,
                            wide: wide,
                            steps:
                                steps[FitnessService.dateKey(selectedDay)] ?? 0,
                            workouts: workouts,
                            selectedDate: selectedDay,
                          ),
                          .08,
                        ),
                        const SizedBox(height: 25),
                        _entrance(
                          wide
                              ? Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Expanded(
                                      flex: 6,
                                      child: _weeklyCard(steps, workouts),
                                    ),
                                    const SizedBox(width: 20),
                                    Expanded(
                                      flex: 4,
                                      child: _activityCard(workouts),
                                    ),
                                  ],
                                )
                              : Column(
                                  children: [
                                    _weeklyCard(steps, workouts),
                                    const SizedBox(height: 18),
                                    _activityCard(workouts),
                                  ],
                                ),
                          .18,
                        ),
                        if (!widget.service.isConnected) ...[
                          const SizedBox(height: 18),
                          _entrance(_demoNotice(), .3),
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
        icon: Icon(Icons.add_rounded),
        label: Text(
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
          '${weekdays[now.weekday - 1]} ${now.day} ${months[now.month - 1]}',
          style: TextStyle(
            color: _muted(context),
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 7),
        Row(
          children: [
            Expanded(
              child: AnimatedSwitcher(
                duration: const Duration(milliseconds: 260),
                child: Text(
                  userName == null || userName!.isEmpty
                      ? 'Bonjour 👋'
                      : 'Bonjour, $userName 👋',
                  key: ValueKey(userName),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    color: _ink(context),
                    fontSize: 29,
                    fontWeight: FontWeight.w800,
                    letterSpacing: -1.1,
                  ),
                ),
              ),
            ),
            if (widget.service.isConnected)
              IconButton(
                tooltip: 'Modifier mon prénom',
                onPressed: _editName,
                visualDensity: VisualDensity.compact,
                icon: Icon(
                  Icons.edit_outlined,
                  size: 18,
                  color: _muted(context),
                ),
              ),
          ],
        ),
        const SizedBox(height: 5),
        Text(
          'Chaque mouvement compte. Voici ton activité.',
          style: TextStyle(color: _muted(context), fontSize: 14),
        ),
      ],
    );
  }

  Future<void> _editName() async {
    final controller = TextEditingController(text: userName ?? '');
    final formKey = GlobalKey<FormState>();
    final name = await showDialog<String>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text('Ton prénom'),
        content: Form(
          key: formKey,
          child: TextFormField(
            controller: controller,
            autofocus: true,
            maxLength: 30,
            textCapitalization: TextCapitalization.words,
            decoration: const InputDecoration(
              labelText: 'Comment t’appeler ?',
              hintText: 'Ex. Nadège',
            ),
            validator: (value) {
              final name = value?.trim() ?? '';
              if (name.isEmpty) return 'Saisis ton prénom pour continuer.';
              return null;
            },
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext),
            child: Text('Annuler'),
          ),
          FilledButton(
            onPressed: () {
              if (formKey.currentState!.validate()) {
                Navigator.pop(dialogContext, controller.text.trim());
              }
            },
            child: Text('Enregistrer'),
          ),
        ],
      ),
    );
    controller.dispose();
    if (name == null || !mounted) return;

    try {
      await widget.service.updateUserName(name);
      if (!mounted) return;
      setState(() => userName = name);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Ton prénom a été enregistré.')),
      );
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Impossible d’enregistrer le prénom : $error')),
      );
    }
  }

  Widget _topCards(
    BuildContext context, {
    required bool wide,
    required int steps,
    required List<Workout> workouts,
    required DateTime selectedDate,
  }) {
    final todaysWorkouts = workouts
        .where((w) => w.date == FitnessService.dateKey(selectedDate))
        .toList();
    final minutes = todaysWorkouts.fold<int>(
      0,
      (runningTotal, workout) => runningTotal + workout.durationMinutes,
    );
    final calories = todaysWorkouts.fold<int>(
      0,
      (runningTotal, workout) => runningTotal + workout.calories,
    );
    final stepCard = _stepsCard(context, steps, selectedDate);

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

  Widget _stepsCard(BuildContext context, int steps, DateTime selectedDate) =>
      Container(
        padding: const EdgeInsets.all(22),
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Color(0xFF10392C), Color(0xFF1D6047)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(25),
          boxShadow: [
            BoxShadow(
              color: green.withValues(alpha: .18),
              blurRadius: 24,
              offset: const Offset(0, 12),
            ),
          ],
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
                      Icon(Icons.directions_walk, color: lime, size: 19),
                      const SizedBox(width: 7),
                      Text(
                        'Pas le ${_shortDate(selectedDate)}',
                        style: TextStyle(
                          color: Colors.white70,
                          fontSize: 13,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      const Spacer(),
                      IconButton(
                        tooltip: 'Saisir le nombre de pas',
                        onPressed: () =>
                            _showStepsDialog(context, steps, selectedDate),
                        visualDensity: VisualDensity.compact,
                        icon: Icon(
                          Icons.edit_outlined,
                          color: Colors.white70,
                          size: 18,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 7),
                  TweenAnimationBuilder<int>(
                    tween: IntTween(begin: 0, end: steps),
                    duration: const Duration(milliseconds: 850),
                    curve: Curves.easeOutCubic,
                    builder: (context, animatedSteps, _) => Text(
                      _number(animatedSteps),
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 38,
                        fontWeight: FontWeight.w800,
                        letterSpacing: -1.5,
                      ),
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    '${_number(stepGoal)} pas par jour',
                    style: TextStyle(color: Colors.white60, fontSize: 12),
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
                  TweenAnimationBuilder<double>(
                    tween: Tween<double>(
                      begin: 0,
                      end: (steps / stepGoal).clamp(0.0, 1.0),
                    ),
                    duration: const Duration(milliseconds: 850),
                    curve: Curves.easeOutCubic,
                    builder: (context, progress, _) => SizedBox.expand(
                      child: CircularProgressIndicator(
                        value: progress,
                        strokeWidth: 9,
                        backgroundColor: Colors.white.withValues(alpha: .16),
                        valueColor: const AlwaysStoppedAnimation(lime),
                        strokeCap: StrokeCap.round,
                      ),
                    ),
                  ),
                  Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      TweenAnimationBuilder<double>(
                        tween: Tween<double>(
                          begin: 0,
                          end: (steps / stepGoal * 100),
                        ),
                        duration: const Duration(milliseconds: 850),
                        curve: Curves.easeOutCubic,
                        builder: (context, percent, _) => Text(
                          '${percent.round()}%',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.w800,
                            fontSize: 21,
                          ),
                        ),
                      ),
                      Text(
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
      color: _panelSurface(context),
      borderRadius: BorderRadius.circular(22),
      border: Border.all(color: _line(context)),
      boxShadow: [
        BoxShadow(
          color: _ink(context).withValues(alpha: .025),
          blurRadius: 18,
          offset: const Offset(0, 6),
        ),
      ],
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
                style: TextStyle(
                  color: _muted(context),
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
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 320),
              transitionBuilder: (child, animation) => FadeTransition(
                opacity: animation,
                child: SlideTransition(
                  position: Tween<Offset>(
                    begin: const Offset(0, .16),
                    end: Offset.zero,
                  ).animate(animation),
                  child: child,
                ),
              ),
              child: Text(
                value,
                key: ValueKey(value),
                style: TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.w800,
                  color: _ink(context),
                  letterSpacing: -1,
                ),
              ),
            ),
            const SizedBox(width: 6),
            Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(
                unit,
                style: TextStyle(color: _muted(context), fontSize: 11),
              ),
            ),
          ],
        ),
      ],
    ),
  );

  Widget _weeklyCard(Map<String, int> steps, List<Workout> workouts) {
    final days = List.generate(
      7,
      (index) => weekStart.add(Duration(days: index)),
    );
    final values = days
        .map((day) => steps[FitnessService.dateKey(day)] ?? 0)
        .toList();
    final total = values.fold<int>(
      0,
      (runningTotal, value) => runningTotal + value,
    );
    final weeklyMinutes = workouts.fold<int>(
      0,
      (runningTotal, workout) => runningTotal + workout.durationMinutes,
    );
    final weeklyCalories = workouts.fold<int>(
      0,
      (runningTotal, workout) => runningTotal + workout.calories,
    );
    final weeklyDistance = workouts.fold<double>(
      0,
      (runningTotal, workout) => runningTotal + (workout.distanceKm ?? 0),
    );
    const labels = ['Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa', 'Di'];

    return _panel(
      title: 'Cette semaine',
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          IconButton(
            tooltip: 'Semaine précédente',
            visualDensity: VisualDensity.compact,
            onPressed: () => _changeWeek(-1),
            icon: Icon(Icons.chevron_left_rounded, size: 20),
          ),
          Text(
            '${weekStart.day}/${weekStart.month}',
            style: TextStyle(
              color: _muted(context),
              fontSize: 10,
              fontWeight: FontWeight.w600,
            ),
          ),
          IconButton(
            tooltip: 'Semaine suivante',
            visualDensity: VisualDensity.compact,
            onPressed: weekStart.isBefore(FitnessService.startOfWeek(today))
                ? () => _changeWeek(1)
                : null,
            icon: Icon(Icons.chevron_right_rounded, size: 20),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            _number(total),
            style: TextStyle(
              fontSize: 28,
              color: _ink(context),
              fontWeight: FontWeight.w800,
              letterSpacing: -1,
            ),
          ),
          Text(
            'pas au total',
            style: TextStyle(color: _muted(context), fontSize: 11),
          ),
          const SizedBox(height: 22),
          SizedBox(
            height: 126,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: List.generate(7, (index) {
                final active =
                    FitnessService.dateKey(days[index]) ==
                    FitnessService.dateKey(today);
                final selected =
                    FitnessService.dateKey(days[index]) ==
                    FitnessService.dateKey(selectedDay);
                final ratio = (values[index] / 10000).clamp(0.05, 1.0);
                return Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 3),
                    child: Material(
                      color: Colors.transparent,
                      child: InkWell(
                        borderRadius: BorderRadius.circular(12),
                        onTap: () => setState(() => selectedDay = days[index]),
                        child: Padding(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 2,
                            vertical: 4,
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              Text(
                                values[index] == 0
                                    ? ''
                                    : _compact(values[index]),
                                style: TextStyle(
                                  color: _muted(context),
                                  fontSize: 9,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                              const SizedBox(height: 7),
                              Expanded(
                                child: Align(
                                  alignment: Alignment.bottomCenter,
                                  child: TweenAnimationBuilder<double>(
                                    tween: Tween<double>(
                                      begin: 0,
                                      end: values[index] == 0 ? .04 : ratio,
                                    ),
                                    duration: const Duration(milliseconds: 650),
                                    curve: Curves.easeOutCubic,
                                    builder: (context, barHeight, _) =>
                                        FractionallySizedBox(
                                          heightFactor: barHeight,
                                          widthFactor: .72,
                                          child: AnimatedContainer(
                                            duration: const Duration(
                                              milliseconds: 220,
                                            ),
                                            decoration: BoxDecoration(
                                              color: selected
                                                  ? green
                                                  : active
                                                  ? lime
                                                  : Theme.of(context)
                                                        .colorScheme
                                                        .surfaceContainerHighest,
                                              borderRadius:
                                                  BorderRadius.circular(9),
                                            ),
                                          ),
                                        ),
                                  ),
                                ),
                              ),
                              const SizedBox(height: 9),
                              Text(
                                '${labels[index]} ${days[index].day}',
                                style: TextStyle(
                                  color: selected || active
                                      ? green
                                      : _muted(context),
                                  fontSize: 10,
                                  fontWeight: selected || active
                                      ? FontWeight.w800
                                      : FontWeight.w500,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                );
              }),
            ),
          ),
          const SizedBox(height: 9),
          Text(
            'Touche une journée pour consulter ses détails.',
            style: TextStyle(color: _muted(context), fontSize: 10),
          ),
          const SizedBox(height: 18),
          Row(
            children: [
              Expanded(
                child: _weekMetric(
                  icon: Icons.fitness_center_rounded,
                  label: 'Séances',
                  value: workouts.length.toString(),
                  subtitle: weeklyDistance > 0
                      ? '${weeklyDistance.toStringAsFixed(1)} km parcourus'
                      : null,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _weekMetric(
                  icon: Icons.timer_outlined,
                  label: 'Minutes',
                  value: weeklyMinutes.toString(),
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _weekMetric(
                  icon: Icons.local_fire_department_outlined,
                  label: 'Calories',
                  value: _compact(weeklyCalories),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _weekMetric({
    required IconData icon,
    required String label,
    required String value,
    String? subtitle,
  }) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 11),
    decoration: BoxDecoration(
      color: _softSurface(context),
      borderRadius: BorderRadius.circular(13),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Icon(icon, size: 15, color: green),
        const SizedBox(height: 8),
        Text(
          value,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            color: _ink(context),
            fontSize: 16,
            fontWeight: FontWeight.w800,
          ),
        ),
        Text(
          label,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(color: _muted(context), fontSize: 9),
        ),
        if (subtitle != null) ...[
          const SizedBox(height: 3),
          Text(
            subtitle,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(color: green, fontSize: 8),
          ),
        ],
      ],
    ),
  );

  Widget _activityCard(List<Workout> workouts) {
    final dayKey = FitnessService.dateKey(selectedDay);
    final visible = workouts
        .where((workout) => workout.date == dayKey)
        .toList();

    return _panel(
      title: 'Séances du ${_shortDate(selectedDay)}',
      trailing: Text(
        visible.length.toString() +
            (visible.length == 1 ? ' séance' : ' séances'),
        style: TextStyle(
          color: _muted(context),
          fontSize: 11,
          fontWeight: FontWeight.w600,
        ),
      ),
      child: visible.isEmpty
          ? Padding(
              padding: const EdgeInsets.symmetric(vertical: 24),
              child: Center(
                child: Text(
                  'Aucune séance ce jour. Ajoute une activité pour la noter.',
                  style: TextStyle(color: _muted(context), fontSize: 12),
                ),
              ),
            )
          : Column(
              children: [
                for (var i = 0; i < visible.length; i++) ...[
                  _workoutRow(
                    visible[i],
                    onEdit: () =>
                        _showWorkoutForm(context, workout: visible[i]),
                    onDelete: () => _deleteWorkout(visible[i]),
                  ),
                  if (i != visible.length - 1)
                    Divider(height: 18, color: _line(context)),
                ],
              ],
            ),
    );
  }

  Widget _workoutRow(
    Workout workout, {
    required VoidCallback onEdit,
    required VoidCallback onDelete,
  }) {
    final details = [
      '${workout.durationMinutes} min',
      '${workout.calories} kcal',
      if (workout.distanceKm != null)
        '${workout.distanceKm!.toStringAsFixed(1)} km',
      if (workout.heartRateBpm != null) '${workout.heartRateBpm} bpm',
      if (workout.sets != null && workout.repetitions != null)
        '${workout.sets} × ${workout.repetitions}',
    ].join('  ·  ');
    final note = workout.notes?.trim();
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
            color: Theme.of(context).colorScheme.surfaceContainerHighest,
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
                style: TextStyle(
                  color: _ink(context),
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
              const SizedBox(height: 4),
              Text(
                details,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: _muted(context), fontSize: 10),
              ),
              if (note != null && note.isNotEmpty) ...[
                const SizedBox(height: 3),
                Text(
                  note,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(color: _muted(context), fontSize: 9),
                ),
              ],
            ],
          ),
        ),
        IconButton(
          tooltip: 'Modifier la séance',
          onPressed: onEdit,
          visualDensity: VisualDensity.compact,
          icon: Icon(Icons.edit_outlined, size: 18, color: _muted(context)),
        ),
        IconButton(
          tooltip: 'Supprimer la séance',
          onPressed: onDelete,
          visualDensity: VisualDensity.compact,
          icon: Icon(Icons.delete_outline, size: 18, color: _muted(context)),
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
      color: _panelSurface(context),
      border: Border.all(color: _line(context)),
      borderRadius: BorderRadius.circular(23),
      boxShadow: [
        BoxShadow(
          color: green.withValues(alpha: .035),
          blurRadius: 26,
          offset: const Offset(0, 9),
        ),
      ],
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Expanded(
              child: Text(
                title,
                style: TextStyle(
                  color: _ink(context),
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
      color: Theme.of(context).colorScheme.tertiaryContainer,
      borderRadius: BorderRadius.circular(15),
      border: Border.all(color: Theme.of(context).colorScheme.outlineVariant),
    ),
    child: Row(
      children: [
        Icon(
          Icons.info_outline,
          color: Theme.of(context).colorScheme.onTertiaryContainer,
          size: 18,
        ),
        const SizedBox(width: 10),
        Expanded(
          child: Text(
            widget.service.connectionError ??
                'Mode aperçu : les modifications ne sont pas enregistrées. Configure Firebase pour activer la sauvegarde.',
            style: TextStyle(
              color: Theme.of(context).colorScheme.onTertiaryContainer,
              fontSize: 11,
              height: 1.4,
            ),
          ),
        ),
      ],
    ),
  );

  Future<void> _showStepsDialog(
    BuildContext context,
    int current,
    DateTime date,
  ) async {
    final value = await showDialog<int>(
      context: context,
      builder: (_) => StepsDialog(current: current, date: date),
    );
    if (value == null || !mounted) return;

    try {
      await widget.service.setStepsForDate(date, value);
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        this.context,
      ).showSnackBar(SnackBar(content: Text(_saveErrorMessage(error))));
    }
  }

  Future<void> _showWorkoutForm(
    BuildContext context, {
    Workout? workout,
  }) async {
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (_) => WorkoutFormSheet(
        service: widget.service,
        initialDate: selectedDay,
        workout: workout,
      ),
    );
  }

  Future<void> _deleteWorkout(Workout workout) async {
    final shouldDelete = await showDialog<bool>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: Text('Supprimer cette séance ?'),
        content: Text('Cette action supprimera « ${workout.type} ».'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogContext, false),
            child: Text('Annuler'),
          ),
          FilledButton.tonal(
            onPressed: () => Navigator.pop(dialogContext, true),
            child: Text('Supprimer'),
          ),
        ],
      ),
    );
    if (shouldDelete != true || !mounted) return;
    try {
      await widget.service.deleteWorkout(workout.id);
    } catch (error) {
      if (!mounted) return;
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text(_saveErrorMessage(error))));
    }
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
      ? '${(value / 1000).toStringAsFixed(1)}k'
      : value.toString();
}

class StepsDialog extends StatefulWidget {
  const StepsDialog({required this.current, required this.date, super.key});

  final int current;
  final DateTime date;

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
    title: Text('Saisir tes pas · ${_shortDate(widget.date)}'),
    content: Form(
      key: formKey,
      child: TextFormField(
        controller: controller,
        autofocus: true,
        keyboardType: TextInputType.number,
        decoration: const InputDecoration(
          labelText: 'Nombre de pas pour ce jour',
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
        child: Text('Annuler'),
      ),
      FilledButton(
        onPressed: () {
          if (formKey.currentState!.validate()) {
            Navigator.pop(context, int.parse(controller.text.trim()));
          }
        },
        child: Text('Enregistrer'),
      ),
    ],
  );
}

class WorkoutFormSheet extends StatefulWidget {
  const WorkoutFormSheet({
    required this.service,
    required this.initialDate,
    this.workout,
    super.key,
  });

  final FitnessService service;
  final DateTime initialDate;
  final Workout? workout;

  @override
  State<WorkoutFormSheet> createState() => _WorkoutFormSheetState();
}

class _WorkoutFormSheetState extends State<WorkoutFormSheet> {
  final formKey = GlobalKey<FormState>();
  final durationController = TextEditingController();
  final caloriesController = TextEditingController();
  final distanceController = TextEditingController();
  final heartRateController = TextEditingController();
  final setsController = TextEditingController();
  final repetitionsController = TextEditingController();
  final notesController = TextEditingController();
  late String exercise;
  late DateTime date;
  bool saving = false;

  static const exercises = [
    'Course',
    'Marche',
    'Vélo',
    'Musculation',
    'Yoga',
    'Course à pied',
    'Cyclisme',
    'Morning run',
    'Strength training',
    'Cycling',
    'Autre',
  ];

  @override
  void initState() {
    super.initState();
    final workout = widget.workout;
    durationController.text = workout?.durationMinutes.toString() ?? '';
    caloriesController.text = workout?.calories.toString() ?? '';
    distanceController.text = workout?.distanceKm?.toString() ?? '';
    heartRateController.text = workout?.heartRateBpm?.toString() ?? '';
    setsController.text = workout?.sets?.toString() ?? '';
    repetitionsController.text = workout?.repetitions?.toString() ?? '';
    notesController.text = workout?.notes ?? '';
    exercise = workout?.type ?? 'Course';
    date = workout == null
        ? widget.initialDate
        : DateTime.tryParse(workout.date) ?? widget.initialDate;
  }

  @override
  void dispose() {
    durationController.dispose();
    caloriesController.dispose();
    distanceController.dispose();
    heartRateController.dispose();
    setsController.dispose();
    repetitionsController.dispose();
    notesController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final bottomInset = MediaQuery.viewInsetsOf(context).bottom;
    return Container(
      padding: EdgeInsets.fromLTRB(22, 12, 22, 22 + bottomInset),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surface,
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
                    color: _line(context),
                    borderRadius: BorderRadius.circular(4),
                  ),
                ),
              ),
              const SizedBox(height: 22),
              Text(
                widget.workout == null
                    ? 'Nouvelle séance'
                    : 'Modifier la séance',
                style: TextStyle(
                  color: _ink(context),
                  fontSize: 22,
                  fontWeight: FontWeight.w800,
                  letterSpacing: -.5,
                ),
              ),
              const SizedBox(height: 5),
              Text(
                'Ajoute les détails de ton activité.',
                style: TextStyle(color: _muted(context), fontSize: 13),
              ),
              const SizedBox(height: 22),
              DropdownButtonFormField<String>(
                initialValue: exercise,
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
                  if (value != null) {
                    setState(() {
                      exercise = value;
                      if (!_isStrengthExercise) {
                        setsController.clear();
                        repetitionsController.clear();
                      }
                    });
                  }
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
              Container(
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: _line(context)),
                ),
                child: ExpansionTile(
                  tilePadding: const EdgeInsets.symmetric(horizontal: 13),
                  childrenPadding: const EdgeInsets.fromLTRB(13, 0, 13, 14),
                  leading: Icon(Icons.tune_rounded, color: green),
                  title: Text(
                    'Détails supplémentaires',
                    style: TextStyle(
                      color: _ink(context),
                      fontSize: 13,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  subtitle: Text(
                    'Facultatifs : distance, rythme, notes…',
                    style: TextStyle(color: _muted(context), fontSize: 10),
                  ),
                  children: [
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: distanceController,
                            keyboardType: const TextInputType.numberWithOptions(
                              decimal: true,
                            ),
                            decoration: const InputDecoration(
                              labelText: 'Distance',
                              suffixText: 'km',
                              border: OutlineInputBorder(),
                              errorMaxLines: 2,
                            ),
                            validator: _validateDistance,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: TextFormField(
                            controller: heartRateController,
                            keyboardType: TextInputType.number,
                            decoration: const InputDecoration(
                              labelText: 'Fréquence cardiaque',
                              suffixText: 'bpm',
                              border: OutlineInputBorder(),
                              errorMaxLines: 2,
                            ),
                            validator: _validateHeartRate,
                          ),
                        ),
                      ],
                    ),
                    if (_isStrengthExercise) ...[
                      const SizedBox(height: 12),
                      Row(
                        children: [
                          Expanded(
                            child: TextFormField(
                              controller: setsController,
                              keyboardType: TextInputType.number,
                              decoration: const InputDecoration(
                                labelText: 'Séries',
                                border: OutlineInputBorder(),
                                errorMaxLines: 2,
                              ),
                              validator: (value) => _validatePairedCount(
                                value,
                                otherValue: repetitionsController.text,
                                otherLabel: 'répétitions',
                                fieldLabel: 'séries',
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: TextFormField(
                              controller: repetitionsController,
                              keyboardType: TextInputType.number,
                              decoration: const InputDecoration(
                                labelText: 'Répétitions',
                                border: OutlineInputBorder(),
                                errorMaxLines: 2,
                              ),
                              validator: (value) => _validatePairedCount(
                                value,
                                otherValue: setsController.text,
                                otherLabel: 'séries',
                                fieldLabel: 'répétitions',
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: notesController,
                      maxLength: 300,
                      maxLines: 3,
                      decoration: const InputDecoration(
                        labelText: 'Notes (facultatif)',
                        hintText: 'Comment s’est passée ta séance ?',
                        alignLabelWithHint: true,
                        border: OutlineInputBorder(),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),
              OutlinedButton.icon(
                onPressed: _pickDate,
                icon: Icon(Icons.calendar_today_outlined, size: 17),
                label: Text(
                  date.year == DateTime.now().year &&
                          date.month == DateTime.now().month &&
                          date.day == DateTime.now().day
                      ? 'Aujourd’hui'
                      : '${date.day}/${date.month}/${date.year}',
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
                      : Icon(Icons.check_rounded),
                  label: Text(
                    saving
                        ? 'Enregistrement…'
                        : widget.workout == null
                        ? 'Enregistrer la séance'
                        : 'Enregistrer les modifications',
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

  bool get _isStrengthExercise =>
      exercise.toLowerCase().contains('musculation') ||
      exercise.toLowerCase().contains('strength');

  String? _validateDistance(String? value) {
    final text = value?.trim() ?? '';
    if (text.isEmpty) return null;
    final distance = double.tryParse(text.replaceAll(',', '.'));
    if (distance == null) {
      return 'Entre une distance valide (ex. 2,5).';
    }
    if (distance <= 0) return 'La distance doit être supérieure à 0.';
    return null;
  }

  String? _validateHeartRate(String? value) {
    final text = value?.trim() ?? '';
    if (text.isEmpty) return null;
    final heartRate = int.tryParse(text);
    if (heartRate == null) return 'Entre un nombre entier de battements.';
    if (heartRate < 30 || heartRate > 240) {
      return 'La fréquence doit être comprise entre 30 et 240 bpm.';
    }
    return null;
  }

  String? _validatePairedCount(
    String? value, {
    required String otherValue,
    required String otherLabel,
    required String fieldLabel,
  }) {
    final text = value?.trim() ?? '';
    final otherText = otherValue.trim();
    if (text.isEmpty && otherText.isEmpty) return null;
    if (text.isEmpty) return 'Indique aussi le nombre de $fieldLabel.';
    final count = int.tryParse(text);
    if (count == null) return 'Le nombre de $fieldLabel doit être entier.';
    if (count <= 0) return 'Le nombre de $fieldLabel doit être supérieur à 0.';
    if (otherText.isEmpty) return 'Indique aussi le nombre de $otherLabel.';
    final otherCount = int.tryParse(otherText);
    if (otherCount == null) return 'Le nombre de $otherLabel doit être entier.';
    if (otherCount <= 0) {
      return 'Le nombre de $otherLabel doit être supérieur à 0.';
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
      final duration = int.parse(durationController.text.trim());
      final calories = int.parse(caloriesController.text.trim());
      final distanceText = distanceController.text.trim().replaceAll(',', '.');
      final distance = distanceText.isEmpty ? null : double.parse(distanceText);
      final heartRate = heartRateController.text.trim().isEmpty
          ? null
          : int.parse(heartRateController.text.trim());
      final sets = setsController.text.trim().isEmpty
          ? null
          : int.parse(setsController.text.trim());
      final repetitions = repetitionsController.text.trim().isEmpty
          ? null
          : int.parse(repetitionsController.text.trim());
      final notes = notesController.text.trim();
      final existingWorkout = widget.workout;
      if (existingWorkout == null) {
        await widget.service.addWorkout(
          type: exercise,
          duration: duration,
          calories: calories,
          date: date,
          distanceKm: distance,
          heartRateBpm: heartRate,
          sets: sets,
          repetitions: repetitions,
          notes: notes.isEmpty ? null : notes,
        );
      } else {
        await widget.service.updateWorkout(
          id: existingWorkout.id,
          type: exercise,
          duration: duration,
          calories: calories,
          date: date,
          distanceKm: distance,
          heartRateBpm: heartRate,
          sets: sets,
          repetitions: repetitions,
          notes: notes.isEmpty ? null : notes,
        );
      }
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
