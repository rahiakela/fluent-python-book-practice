from concurrent import futures
from flags import save_flag, get_flag, show, main

# Maximum number of threads to be used in the ThreadPoolExecutor.
MAX_WORKERS = 20


"""
Note that the download_one function is essentially the body of the for loop in 
the download_many function of flags.py.
This is a common refactoring when writing concurrent code: turning the body of a sequential
loop into a for function to be called concurrently.
"""
def download_one(cc):
    """download a single image; this is what each thread will execute."""
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + ".gif")

    return cc


def download_many(cc_list):
    """
    Set the number of worker threads: use the smaller number between the
    maximum we want to allow (MAX_WORKERS) and the actual items to be
    processed, so no unnecessary threads are created.
    """
    workers = min(MAX_WORKERS, len(cc_list))

    # Instantiate the ThreadPoolExecutor with that number of worker threads
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


if __name__ == '__main__':
    # Call the main function from the flags module, passing the enhanced version of download_many.
    main(download_many)
