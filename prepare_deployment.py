import os
import shutil
import sys

def prepare_vector_database():
    """Prepare the vector database for deployment"""
    print("🔄 Preparing vector database for deployment...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source and destination paths
    source_db_path = os.path.join(current_dir, "chroma_store")
    api_dir = os.path.join(current_dir, "api")
    dest_db_path = os.path.join(api_dir, "chroma_store")
    
    # Check if source database exists
    if not os.path.exists(source_db_path):
        print("❌ Error: Vector database not found at", source_db_path)
        print("   Please run scripts/embed_and_store.py first to create the database.")
        return False
    
    # Create api directory if it doesn't exist
    if not os.path.exists(api_dir):
        os.makedirs(api_dir)
        print("📁 Created API directory")
    
    # Remove existing database in api directory if it exists
    if os.path.exists(dest_db_path):
        print("🗑️ Removing existing database in API directory")
        shutil.rmtree(dest_db_path)
    
    # Copy the database to the api directory
    print(f"📦 Copying database from {source_db_path} to {dest_db_path}")
    shutil.copytree(source_db_path, dest_db_path)
    
    # Verify the copy
    if os.path.exists(dest_db_path):
        print("✅ Vector database successfully prepared for deployment")
        return True
    else:
        print("❌ Failed to copy vector database")
        return False

def prepare_data_files():
    """Prepare data files for deployment"""
    print("🔄 Preparing data files for deployment...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source and destination paths
    source_data_path = os.path.join(current_dir, "data")
    api_dir = os.path.join(current_dir, "api")
    dest_data_path = os.path.join(api_dir, "data")
    
    # Check if source data exists
    if not os.path.exists(source_data_path):
        print("❌ Error: Data directory not found at", source_data_path)
        return False
    
    # Create api directory if it doesn't exist
    if not os.path.exists(api_dir):
        os.makedirs(api_dir)
        print("📁 Created API directory")
    
    # Remove existing data in api directory if it exists
    if os.path.exists(dest_data_path):
        print("🗑️ Removing existing data in API directory")
        shutil.rmtree(dest_data_path)
    
    # Copy the data to the api directory
    print(f"📦 Copying data from {source_data_path} to {dest_data_path}")
    shutil.copytree(source_data_path, dest_data_path)
    
    # Verify the copy
    if os.path.exists(dest_data_path):
        print("✅ Data files successfully prepared for deployment")
        return True
    else:
        print("❌ Failed to copy data files")
        return False

def main():
    print("🚀 Starting deployment preparation...\n")
    
    # Prepare vector database
    db_success = prepare_vector_database()
    
    # Prepare data files
    data_success = prepare_data_files()
    
    if db_success and data_success:
        print("\n✅ All preparations completed successfully!")
        print("📝 You can now deploy the application to Vercel using:")
        print("   ./deploy.sh")
        return 0
    else:
        print("\n❌ Preparation failed. Please fix the errors and try again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())