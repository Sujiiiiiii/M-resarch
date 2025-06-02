import os
import shutil


def delete_test_debug_folders(directory: str) -> None:
    for foldername in os.listdir(directory):
        folder_path = os.path.join(directory, foldername)

        if os.path.isdir(folder_path) and (
            "test" in foldername.lower()
            or "debug" in foldername.lower()
            or "eval" in foldername.lower()
        ):
            print(f"deleted: {folder_path}")
            shutil.rmtree(folder_path)


if __name__ == "__main__":
    results_dir = "./results"
    delete_test_debug_folders(results_dir)
    print("Done.")
