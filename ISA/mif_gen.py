def generate_mif(width: int, depth: int, filename: str, data: list[int]):
	f = open(filename + ".mif", "w")
	f.write(f"-- Quartus Prime generated Memory Initialization File (.mif)\n\nWIDTH={width};\nDEPTH={depth};\n\nADDRESS_RADIX=UNS;\nDATA_RADIX=UNS;\n\nCONTENT BEGIN\n")
	while (len(data)):
		if data[-1]:
			break
		else:
			data.pop()
	s = 0
	e = 1
	while (e < len(data)):
		if data[s] != data[e] or e == len(data) - 1:
			if s == e - 1:
				f.write(f"\t{s}:\t{data[s]};\n")
				if (e == len(data) - 1):
					f.write(f"\t{e}:\t{data[e]};\n")
			else:
				f.write(f"\t[{s}..{e - 1}]:\t{data[s]};\n")
			s = e
		e += 1
	if e < depth:
		if s == depth:
			f.write(f"\t{e - 1}:\t0;\n")
		else:
			f.write(f"\t[{e - 1}..{depth - 1}]:\t0;\n")
	f.write("END;\n")
	f.close()

#tests
generate_mif(32, 4096, "Mif3", [127105, 140, 0])
#generate_mif(32, 4096, "test_mif", [0, 1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0])
#generate_mif(32, 4096, "test_mif", [])

#ALU test code
generate_mif(32, 4096, "alu_test", [
	(0 << 12) | 1,										#reg[0] = literal
	(10 << 12) | (1 << 7) | 1,							#reg[1] = 10
	(1 << 12) | (2 << 7) | 3,							#reg[2] = reg[1]
	(2 << 7) | (1 << 3) | 4,							#write reg[2] to ram as copy operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (1 << 3) | 3,	#reg[3] = reg[1] + reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as add operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (2 << 3) | 3,	#reg[3] = reg[2] - reg[1]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(1 << 12) | (3 << 7) | (3 << 3) | 3,				#reg[3] = ~reg[1]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal



	(2 << 17) | (1 << 12) | (3 << 7) | (5 << 3) | 3,	#reg[3] = reg[1] | reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (6 << 3) | 3,	#reg[3] = reg[1] ^ reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(1 << 12) | (3 << 7) | (7 << 3) | 3,				#reg[3] = reg[1] << 1
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
	(2 << 17) | (1 << 12) | (3 << 7) | (4 << 3) | 3,	#reg[3] = reg[1] & reg[2]
	(2 << 7) | (1 << 3) | 4,							#write reg[3] to ram as sub operation check
	(1 << 17) | (1 << 3) | 3,							#reg[0] = reg[0] + literal
])
