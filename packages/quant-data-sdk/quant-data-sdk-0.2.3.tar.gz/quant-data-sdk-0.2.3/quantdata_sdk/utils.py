import re


def clean_query(query):
    query = re.sub(r"\n", "", query)
    return query


def rand_weights(n):
    """ Produces n random weights that sum to 1 """
    k = np.random.rand(n)
    return k / sum(k)


class WindowException(AttributeError):
	pass
