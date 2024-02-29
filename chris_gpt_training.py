from constants import CLIENT, DATA_DIRECTORY


JSONL_FILE = DATA_DIRECTORY / "Finx_completed_dataset.jsonl"
MODEL = "gpt-3.5-turbo-1106"
SUFFIX = "chris_gpt"


# File related methods
file = CLIENT.files.create(file=open(JSONL_FILE, "rb"), purpose="fine-tune")

print(CLIENT.files.list(purpose="fine-tune"))

# CLIENT.files.delete(file.id)


# Fine-tuning-job related methods
fine_tuning_job = CLIENT.fine_tuning.jobs.create(
    model=MODEL,
    training_file=file.id,
    hyperparameters={"n_epochs": 3},
    suffix=SUFFIX,
)

# CLIENT.fine_tuning.jobs.list()

print(CLIENT.fine_tuning.jobs.retrieve(fine_tuning_job.id))

# CLIENT.fine_tuning.jobs.cancel(fine_tuning_job.id)


# Fine-tuned-model related methods
# CLIENT.models.delete("model_id_here")
