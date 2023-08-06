import quapy as qp
import quapy.functional as F
from sklearn.linear_model import LogisticRegression

qp.environ["SAMPLE_SIZE"] = 500
dataset = qp.datasets.fetch_reviews('hp', tfidf=True, min_df=5)

training = dataset.training
test = dataset.test

lr = LogisticRegression()
pacc = qp.method.aggregative.PACC(lr)

pacc.fit(training)

df = qp.evaluation.artificial_sampling_report(
    pacc,  # the quantification method
    test,  # the test set on which the method will be evaluated
    sample_size=500,  # indicates the size of samples to be drawn
    eval_budget=1000,  # total number of samples to generate
    n_repetitions=10,  # number of samples for each prevalence
    n_jobs=-1,  # the number of parallel workers (-1 for all CPUs)
    random_seed=42,  # allows replicating test samples across runs
    error_metrics=['mae', 'mrae', 'mkld'],  # evaluation metrics
    verbose=True  # set to True to show some standard-line outputs
)