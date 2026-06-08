import re

STD = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRYPTOS = "KRYPTOSABCDEFGHIJLMNQUVWXZ"

PAIRS = {
    "A": (
        "EGYPT TRIP MESSAGE HIDES EAST NORTHEAST PAST A FALLEN WALL "
        "WHERE WORLD TIME BERLIN CLOCK DELIVERS THE FINAL MESSAGE",
        "CACHE LIES MESSAGE HIDES SITE SOMEWHERE PAST A BURIED WALL "
        "WHERE STONE TIME COPPER FIELD DELIVERS THE FINAL MESSAGE",
    ),
    "B": (
        "A KRYPTOS CIPHER MESSAGE EAST NORTHEAST WHERE EGYPT WALL "
        "AND WORLD TIME MET BERLIN CLOCK DELIVERS THE FINAL MESSAGE",
        "A KRYPTOS CIPHER MESSAGE EAST NORTHEAST WHERE EARTH MAGNETIC "
        "FIELD POINTS BERLIN CLOCK SHOWS WHERE CACHE IS BURIED",
    ),
    "C": (
        "MY HIDDEN CIPHER MESSAGE EAST NORTHEAST WHERE EGYPT WALL "
        "AND WORLD TIME MET BERLIN CLOCK SHOWS WHERE HIDDEN PLACE IS",
        "MY HIDDEN CIPHER MESSAGE EAST NORTHEAST WHERE EARTH MAGNETIC "
        "FIELD POINTS BERLIN CLOCK SHOWS WHERE CACHE IS BURIED",
    ),
    "D": (
        "COUNT LIGHT FIELDS TO USE EAST NORTHEAST LIGHT FIELDS GIVE "
        "THE HIDDEN ROUTE BERLIN CLOCK DELIVERS THE FINAL MESSAGE",
        "COUNT LIGHT FIELDS TO USE EAST NORTHEAST LIGHT FIELDS MARK "
        "THE BURIED CACHE BERLIN CLOCK SHOWS WHERE CACHE IS BURIED",
    ),
}


def norm(text):
    return re.sub(r"[^A-Z]", "", text.upper())


def residues(ciphertext, plaintext, alphabet):
    index = {ch: i for i, ch in enumerate(alphabet)}
    return "".join(
        alphabet[(index[c] - index[p]) % 26]
        for c, p in zip(ciphertext, plaintext)
    )


def intervals(text):
    position = 1
    result = []
    for word in text.split():
        nword = norm(word)
        result.append((nword, position, position + len(nword) - 1))
        position += len(nword)
    return result


def main():
    for name, (p4, q5) in PAIRS.items():
        n4, n5 = norm(p4), norm(q5)
        assert len(n4) == 97, (name, "K4 length", len(n4))
        assert len(n5) == 97, (name, "K5 length", len(n5))
        assert n4[21:34] == "EASTNORTHEAST", (name, "first crib")
        assert n4[63:74] == "BERLINCLOCK", (name, "second crib")

    top4, top5 = PAIRS["A"]
    assert norm(top5)[21:34] == "SITESOMEWHERE"
    assert norm(top5)[63:74] == "COPPERFIELD"

    shared = [
        left for left, right in zip(intervals(top4), intervals(top5))
        if left == right
    ]
    assert shared == [
        ("MESSAGE", 10, 16),
        ("HIDES", 17, 21),
        ("PAST", 35, 38),
        ("A", 39, 39),
        ("WALL", 46, 49),
        ("WHERE", 50, 54),
        ("TIME", 60, 63),
        ("DELIVERS", 75, 82),
        ("THE", 83, 85),
        ("FINAL", 86, 90),
        ("MESSAGE", 91, 97),
    ]

    assert residues("FLRVQQPRNGKSS", "EASTNORTHEAST", STD) == "BLZCDCYYGCKAZ"
    assert residues("NYPVTTMZFPK", "BERLINCLOCK", STD) == "MUYKLGKORNA"
    assert residues("FLRVQQPRNGKSS", "EASTNORTHEAST", KRYPTOS) == "RDUMRIYWOYNKY"
    assert residues("NYPVTTMZFPK", "BERLINCLOCK", KRYPTOS) == "ELYOIECBAQK"
    print("Appendix A audit passed")


if __name__ == "__main__":
    main()
