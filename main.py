from itertools import cycle
from typing import Dict


def singleByteXor(text: bytearray, b: int) -> bytearray:
    out = bytearray()

    for i in text:
        out.append(i ^ b)

    return out


def vigenere(text: bytearray, key: bytearray) -> bytearray:
    out = bytearray()

    for i, j in zip(text, cycle(key)):
        out.append(i ^ j)

    return out


def write_ctext_file(ptext: str, key: bytearray, fname: str) -> None:
    pbytes = bytearray(ptext, 'utf-8')
    cbytes = singleByteXor(pbytes, key)

    with open(fname, 'wb') as f:
        f.write(cbytes)


def read_ctext_file(key: bytearray, fname: str) -> bytearray:
    with open(fname, 'rb') as f:
        cbytes = bytearray(f.read())
        ptext = vigenere(cbytes, key)
        return ptext


def byte_counts(data: bytearray) -> Dict[int, int]:
    out = {b: 0 for b in data}  # Initialize a count of zero for each byte that appears in the data.
    for b in data:
        out[b] += 1  # Count how many times each byte appears.
    return out


def byte_ranks(data: bytearray) -> bytearray:
    counts = sorted(byte_counts(data).items(),  # Convert dictionary to a list of tuples
                    key=lambda item: item[1],  # Sort on the second item in the tuple (the count)
                    reverse=True  # Reverse order (more common bytes first)
                    )
    return bytearray([k[0] for k in counts])  # Throw away the counts, return bytes as a bytearray


def english_score(test: bytearray, english: bytearray, penalty=1000) -> int:
    return sum([english.index(b) if b in english  # The score of a byte is its position in the english ranks
                else penalty  # If a character does not appear in english then assign a high score
                for b in test])  # Add up the scores from each individual byte in test


def gen_english_ranks(infile='pg2701.txt') -> bytearray:
    with open('pg2701.txt', 'rb') as f:
        data = f.read()
    return byte_ranks(data)


def break_single_byte(cbytes: bytearray, eng_ranks: bytearray) -> (int, bytearray):
    best = 999999999
    best_byte = 0
    for i in range(0, 255):
        score = english_score(singleByteXor(cbytes, i), eng_ranks)
        if score < best:
            best = score
            best_byte = i
    return best_byte, singleByteXor(cbytes, best_byte)

def break_vigenere(cbytes, eng_ranks, num_bytes=4):
  key = bytearray()
  for i in range(num_bytes):
    key_part = bytearray()
    for x in range(i, len(cbytes), num_bytes):
      key_part.append(cbytes[x])
    key.append(break_single_byte(key_part, eng_ranks)[0])
  return vigenere(cbytes, key)
      
    
def main():
  cbytes = read_ctext_file([0b00000000], 'breakme2.bin')
  eng_ranks = gen_english_ranks()
  message = break_vigenere(cbytes, eng_ranks, 4)
  print(message.decode('utf-8'))

  


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
