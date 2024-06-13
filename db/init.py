from .database import ExerciseManager, UserProgressManager

def init_db(db_path='english_bot.db'):
    exercise_manager = ExerciseManager(db_path)
    user_progress_manager = UserProgressManager(db_path)

    exercise_manager.init_tables()
    user_progress_manager.init_tables()

    return exercise_manager, user_progress_manager
