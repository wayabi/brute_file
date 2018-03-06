import sys
import os
import csv
import ntpath

prefix_ = "##"
suffix_ = "##"
out_dir_ = "./out"

def recursive_replace(base_file_name, base_content, brute, index_key, out_dir):
	key = brute[index_key][0]
	for brute0 in brute[index_key][1]:
		r_content = brute0[0]
		r_content_file = brute0[1]
		file_name = base_file_name.replace("%s%s%s" % (prefix_, key, suffix_), r_content_file) 
		content = base_content.replace("%s%s%s" % (prefix_, key, suffix_), r_content)
		ik = index_key + 1
		if ik == len(brute):
			with open("%s/%s" % (out_dir, file_name), "w") as f:
				f.write(content)
				print(file_name)
		else:
			recursive_replace(file_name, content, brute, ik, out_dir)

if __name__ == "__main__":

	args = sys.argv
	if len(args) < 3:
		print("%s <base_file> <all_content>" % args[0])
		sys.exit()

	base_file_path = args[1]
	brute_file_path = args[2]

	base_content = ""
	with open(base_file_path, "r") as f:
		base_content = f.read()
		#print(base_content)

	sss = []
	with open(brute_file_path, "r") as f:
		sss = csv.reader(f)

		brute = []
		for ss in sss:
			key = ss[0]
			ss0 = ss[1].split("-")
			contents = []
			for s in ss0:
				s0 = s.split(":")
				content = s0[0]
				file_content = s0[0]
				if len(s0) >= 2:
					file_content = s0[1]
				#print("%s:%s" % (content, file_content))
				contents.append((content, file_content))
			brute.append((key, contents))

		print(brute)
		file_name = ntpath.basename(base_file_path)
		recursive_replace(file_name, base_content, brute, 0, out_dir_)
