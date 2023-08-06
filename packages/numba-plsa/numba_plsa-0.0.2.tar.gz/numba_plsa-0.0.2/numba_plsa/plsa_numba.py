import numba
import numpy as np


@numba.jit(nopython=True, parallel=True)
def plsa_numba(dt_row, dt_col, dt_val, topic_doc, term_topic, n_iter):
    n_docs, n_topics = topic_doc.shape
    n_terms = term_topic.shape[1]

    nnz = len(dt_val)
    topic_full = np.zeros((nnz, n_topics))

    term_sum = np.zeros((n_topics))
    doc_sum = np.zeros((n_docs))

    for i in range(n_iter):
        ### Expectation ###
        for idx in range(nnz):
            p = np.zeros((n_topics))
            d, t = dt_row[idx], dt_col[idx]
            s = 0
            for z in range(n_topics):
                p[z] = topic_doc[d, z] * term_topic[z, t]
                s += p[z]
            for z in range(n_topics):
                topic_full[idx, z] = p[z] / s
        ### Maximization ###
        topic_doc[:] = 0
        term_topic[:] = 0
        term_sum[:] = 0
        doc_sum[:] = 0
        for idx in range(nnz):
            for z in range(n_topics):
                q = dt_val[idx] * topic_full[idx, z]
                term_topic[z, dt_col[idx]] += q
                term_sum[z] += q
                topic_doc[dt_row[idx], z] += q
                doc_sum[dt_row[idx]] += q
        # Normalize P(topic | doc)
        for d in range(n_docs):
            for z in range(n_topics):
                topic_doc[d, z] /= doc_sum[d]
        # Normalize P(term | topic)
        for z in range(n_topics):
            for t in range(n_terms):
                term_topic[z, t] /= term_sum[z]
