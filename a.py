import sys
import os
import csv
import ntpath

prefix_ = "##"
suffix_ = "##"
out_dir_ = "./out"

def check_if_then(brute, index_history, if_then):
	for it in if_then:
		key = it[0]
		value = it[1]
		#print("%s=%s?" % (key, value))
		for i in range(len(index_history)):
			if index_history[i] < 0:
				continue
			key0 = brute[i][0].split("?")[0]
			value0 = brute[i][1][index_history[i]][0]
			if key == key0:
				if value != value0:
					return False
	return True

def recursive_replace(base_file_name, base_content, brute, index_key, index_history, out_dir):
	ss_key = brute[index_key][0].split("?")
	key = ss_key[0]
	if_then = []
	if len(ss_key) > 1:
		for a in range(1, len(ss_key)):
			ss = ss_key[a].split("=")
			if_then.append((ss[0], ss[1]))

	index_col = -1
	flag_replace = check_if_then(brute, index_history, if_then)
	if flag_replace == True:
		index_col = 0

	for brute0 in brute[index_key][1]:
		r_content = brute0[0]
		r_content_file = brute0[1]

		if flag_replace == True:
			file_name = base_file_name.replace("%s%s%s" % (prefix_, key, suffix_), r_content_file) 
			content = base_content.replace("%s%s%s" % (prefix_, key, suffix_), r_content)
		else:
			file_name = base_file_name
			content = base_content
		ik = index_key + 1
		if ik == len(brute):
			with open("%s/%s" % (out_dir, file_name), "w") as f:
				f.write(content)
				print(file_name)
		else:
			new_history = list(index_history)
			new_history.append(index_col)
			recursive_replace(file_name, content, brute, ik, new_history, out_dir)
		if index_col >= 0:
			index_col = index_col + 1

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
		index_history = []
		recursive_replace(file_name, base_content, brute, 0, index_history, out_dir_)
