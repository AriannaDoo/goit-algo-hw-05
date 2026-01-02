import timeit

# ---------- Boyer–Moore ----------
def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0

    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i

    s = 0
    while s <= n - m:
        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return s
        else:
            shift = j - bad_char.get(text[s + j], -1)
            s += max(1, shift)

    return -1


# ---------- Knuth–Morris–Pratt ----------
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = j = 0

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# ---------- Rabin–Karp ----------
def rabin_karp_search(text, pattern, prime=101):
    m = len(pattern)
    n = len(text)
    h = pow(256, m - 1) % prime

    p = t = 0
    for i in range(m):
        p = (256 * p + ord(pattern[i])) % prime
        t = (256 * t + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (256 * (t - ord(text[i]) * h) + ord(text[i + m])) % prime
            t = (t + prime) % prime
    return -1


# ---------- Utils ----------
def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def benchmark(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=10)


# ---------- Main ----------
if __name__ == "__main__":
    text1 = load_text("article1.txt")
    text2 = load_text("article2.txt")

    existing_pattern = "algorithm"
    fake_pattern = "qwertyuiopasdfgh"

    algorithms = {
        "Boyer–Moore": boyer_moore_search,
        "Knuth–Morris–Pratt": kmp_search,
        "Rabin–Karp": rabin_karp_search,
    }

    for name, text in [("Article 1", text1), ("Article 2", text2)]:
        print(f"\n{name}")
        for alg_name, alg in algorithms.items():
            t_exist = benchmark(alg, text, existing_pattern)
            t_fake = benchmark(alg, text, fake_pattern)
            print(f"{alg_name:25} | existing: {t_exist:.6f}s | fake: {t_fake:.6f}s")
