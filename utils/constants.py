from model.Filter import Filter

all_pass_list = [
    0.7,
    0.7j,
    0.1 + 0.7j,
    1 + 2j,
    0.3 + 0.2j,
    0.5 + 0.5j,
    0.8 + 0.4j,
    0.2 + 0.9j,
    1.5 + 1j,
    0.6 + 0.3j,
    0.4 + 0.6j,
    0.9 + 0.2j,
    1.2 + 0.8j,
    0.5 + 1.5j,
    0.2 + 0.4j,
]


filters = []
butterworthFilter = Filter(
    poles=[
        0.66045672 + 0.44332349j,
        0.66045672 - 0.44332349j,
        0.52429979 + 0.1457741j,
        0.52429979 - 0.1457741j,
    ],
    zeros=[
        -1.00021915 + 0j,
        -0.99999998 + 0.00021913j,
        -0.99999998 - 0.00021913j,
        -0.99978088 + 0j,
    ],
    gain=0.004824343357716228,
)
filters.append({"name": "Butterworth Filter", "filter": butterworthFilter})

chebyshev1Filter = Filter(
    poles=[
        0.78618897 + 0.53451727j,
        0.78618897 - 0.53451727j,
        0.84839427 + 0.2207097j,
        0.84839427 - 0.2207097j,
    ],
    zeros=[
        -1.00021915 + 0j,
        -0.99999998 + 0.00021913j,
        -0.99999998 - 0.00021913j,
        -0.99978088 + 0j,
    ],
    gain=0.0010513933473130974,
)
filters.append({"name": "Chebyshev Type I Filter", "filter": chebyshev1Filter})

chebyshev2Filter = Filter(
    poles=[
        0.81412081 + 0.34216671j,
        0.81412081 - 0.34216671j,
        0.62125795 + 0.15717069j,
        0.62125795 - 0.15717069j,
    ],
    zeros=[
        0.16218512 + 0.98676035j,
        0.16218512 - 0.98676035j,
        0.77985627 + 0.62595862j,
        0.77985627 - 0.62595862j,
    ],
    gain=0.0345589375728779,
)
filters.append({"name": "Chebyshev Type II Filter", "filter": chebyshev2Filter})

ellipticFilter = Filter(
    poles=[
        0.79589405 + 0.56264606j,
        0.79589405 - 0.56264606j,
        0.80810983 + 0.29172164j,
        0.80810983 - 0.29172164j,
    ],
    zeros=[
        0.2901308 + 0.956987j,
        0.2901308 - 0.956987j,
        0.73976805 + 0.67286197j,
        0.73976805 - 0.67286197j,
    ],
    gain=0.041845590593020045,
)
filters.append({"name": "Elliptic Filter", "filter": ellipticFilter})
