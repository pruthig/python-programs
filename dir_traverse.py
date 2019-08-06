import os
import sys

def is_macro_present(macro_to_search, macro_list):
	if len(macro_list)  == 0:
		return False
	else:
		for item in macro_list:
			if item == macro_to_search:
				return True
	return False

if __name__== "__main__":
	count = 0
	# read in all macros
	try:
		file_handle = open("macros.txt", "r")
	except IOError:
		print 'opening failed'
		exit

	file_writer = open("results.txt", "w")

	macro_list = []
	macro_count_dict = {}
	for macro in file_handle:
		macro = macro.strip()
		if not macro:
			continue
		macro_list.append(macro)

	for (dirpath, dirs, files) in os.walk("."):
		if not files:
			continue
		for filename in files:
			path = dirpath + '/' + filename
			if filename.endswith('.h') == False and filename.endswith('.c') == False:
				continue
			while os.path.islink(path) == True:
				path = os.path.dirname(os.path.abspath(path)) + '/' + os.readlink(path)
			try:
				file_handle = open(path, "r")
			except IOError:
				print 'opening failed'
				continue
			found = False
			pre_temp_macro_count = 0
			post_temp_macro_count = 0
			recent_macro = None
			for line_no, line in enumerate(file_handle):
			    trimmed_line = line.strip()
			    if not trimmed_line:
				continue
			    line_strs = trimmed_line.split()
		
			    if line_strs[0] == '#ifndef':
				if found == True:
					post_temp_macro_count += 1
				else:
					pre_temp_macro_count += 1
				continue 
			    elif line_strs[0] == '#ifdef' and len(line_strs) == 2:
				macro_presence_status = is_macro_present(line_strs[1], macro_list)
				if macro_presence_status == False:
					if found == False:
						pre_temp_macro_count += 1
						continue
					else:
						post_temp_macro_count += 1
						continue
				else:
					if found == True:
						post_temp_macro_count += 1
						continue
					else:
						found = True
						file_writer.write('Macro: ' + line_strs[1] + ' found in  ' \
						 + ' ' + path + ' at line number: ' + str(line_no+1) + '\n')
						#print(filename,path, '#ifdef found at', line_no+1)
						line_1 = line_no
						recent_macro = line_strs[1];

			    elif line_strs[0] == '#endif':
				if post_temp_macro_count == 0 and found == True:
					if line_1 != -1:
						#print(filename,path, '#endif found at', line_no+1)
						file_writer.write('Count added for this macro: ' + str(line_no - line_1 + 1) + '\n\n')
						temp_count = line_no - line_1 + 1
						count += temp_count
						if recent_macro in macro_count_dict:
							macro_count_dict[recent_macro] +=  temp_count
						else:
							macro_count_dict[recent_macro] =  temp_count
					
						line_1 = -1
						recent_macro = None
						found = False
						continue
				elif post_temp_macro_count != 0:
					post_temp_macro_count -= 1
					continue
				else:
					if pre_temp_macro_count >= 1:
						pre_temp_macro_count -= 1
						continue
					
			    else:
				None

        file_writer.write('\n\n')
	for key in macro_count_dict:
		file_writer.write("{} = {}".format(key, macro_count_dict[key]) + '\n')
        file_writer.write('\nTotal count is : ', count)

