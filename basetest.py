from heapq import heappush, heappop
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency

def build_frequency_table(text):
    freq_table = defaultdict(int)
    for char in text:
        freq_table[char] += 1
    return freq_table

def build_huffman_tree(freq_table):
    heap = []
    for char, freq in freq_table.items():
        node = HuffmanNode(char, freq)
        heappush(heap, node)
    
    while len(heap) > 1:
        left_node = heappop(heap)
        right_node = heappop(heap)
        merged_freq = left_node.frequency + right_node.frequency
        merged_node = HuffmanNode(None, merged_freq)
        merged_node.left = left_node
        merged_node.right = right_node
        heappush(heap, merged_node)
    
    return heappop(heap)

def build_encoding_table(root):
    encoding_table = {}
    
    def traverse(node, code):
        if node.char is not None:
            encoding_table[node.char] = code
            return
        
        traverse(node.left, code + '0')
        traverse(node.right, code + '1')
    
    traverse(root, '')
    return encoding_table

def compress_text(text, encoding_table):
    compressed_text = ''
    for char in text:
        compressed_text += encoding_table[char]
    return compressed_text

def pad_binary_text(binary_text):
    padding_length = 8 - len(binary_text) % 8
    padded_text = binary_text + '0' * padding_length
    padded_text += format(padding_length, '08b')
    return padded_text

def convert_binary_to_bytes(binary_text):
    bytes_list = []
    for i in range(0, len(binary_text), 8):
        byte = binary_text[i:i+8]
        bytes_list.append(int(byte, 2))
    return bytes(bytes_list)

def huffman_compress(text):
    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    encoding_table = build_encoding_table(huffman_tree)
    compressed_text = compress_text(text, encoding_table)
    padded_text = pad_binary_text(compressed_text)
    compressed_data = convert_binary_to_bytes(padded_text)
    return compressed_data

# 测试文本
text = "测试文本"

# 哈夫曼压缩
compressed_data = huffman_compress(text)

# 输出压缩结果
print(compressed_data)
print("test")
