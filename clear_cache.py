import os
import shutil
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'samplesite.settings')
django.setup()

# Clear database cache
try:
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('DELETE FROM cache_table')
    connection.commit()
    print("✅ Database cache cleared")
except Exception as e:
    print(f"❌ Error clearing database cache: {e}")

# Clear Django default cache
try:
    from django.core.cache import cache
    cache.clear()
    print("✅ Django default cache cleared")
except Exception as e:
    print(f"❌ Error clearing Django default cache: {e}")

# Clear Redis cache if it's configured
try:
    from django.core.cache import caches
    redis_cache = caches['redis']
    redis_cache.clear()
    print("✅ Redis cache cleared")
except Exception as e:
    print(f"❌ Error clearing Redis cache: {e}")

# Clear __pycache__ directories
for root, dirs, files in os.walk('.'):
    for directory in dirs:
        if directory == '__pycache__':
            path = os.path.join(root, directory)
            try:
                shutil.rmtree(path)
                print(f"✅ Removed {path}")
            except Exception as e:
                print(f"❌ Error removing {path}: {e}")

# Clear .pyc files
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            path = os.path.join(root, file)
            try:
                os.remove(path)
                print(f"✅ Removed {path}")
            except Exception as e:
                print(f"❌ Error removing {path}: {e}")

print("\n✅ Cache clearing complete!") 