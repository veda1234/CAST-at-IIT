import math

lmax = (1 - (0.047 * (2.0 ** 0.404) * (3.5 ** 1.883))) * (
                            (4 * 2.0 * 2.0) / (math.pi * math.pi * 1.0)) * math.log(
                    (((0.001 * cd[i]) + ca[i]) / ca[i]) * (4 / math.pi))