import os
import sys
import xlsxwriter


def is_macro_present(macro_to_search, macro_list):
	if len(macro_list)  == 0:
		return False
	else:
		for item in macro_list:
			if item == macro_to_search:
				return True
	return False

def create_xls_file(dict_macros):
    workbook = xlsxwriter.Workbook("Results.xlsx") 
    # add_sheet to workbook
    worksheet = workbook.add_worksheet() 

    cell_format_left = workbook.add_format({ 'align' : 'left'})
    cell_format_right = workbook.add_format({ 'align' : 'right'})

    # set header to bold
    cell_format_left.set_bold(True)
    # Expand columns
    worksheet.set_column('A:A', 25)
    worksheet.set_column('A:B', 15)
    total_count = 0
    i = 0
    worksheet.write(i, 0, "MACRO Name", cell_format_left) 
    worksheet.write(i, 1, "Lines Count", cell_format_left) 
    i += 2

    for key, value in dict_macros.items():
        worksheet.write(i, 0, key, cell_format_left) 
        worksheet.write(i, 1, value, cell_format_right)
        total_count += value
        i += 1

    worksheet.write(i+1, 0, "Total count", cell_format_left)
    worksheet.write(i+1, 1, str(total_count), cell_format_right)
      
    workbook.close()

    
if __name__== "__main__":

	count = 0
        macros_handle = None
        find_all_macros = False
	macro_list = []
        macros_all_set =  set()
	file_writer = open("results.txt", "w")

	try:
		macros_handle = open("macros.txt", "r")
	except:
                macros_handle = open("macros.txt", "w+")
                find_all_macros = True

	macro_count_dict = {}

        if find_all_macros == False:
    	    for macro in macros_handle:
	    	macro = macro.strip()
		if not macro:
			continue
		macro_list.append(macro)

        if find_all_macros == False and  len(macro_list) == 0:
            find_all_macros= True
            macros_handle = open("macros.txt", "w+")

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

                            if line_strs[0] == '#ifdef' and len(line_strs) == 2 and find_all_macros == True:
                                if line_strs[1] not in macros_all_set:
                                    macros_all_set.add(line_strs[1])
                                    continue
		
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

        if find_all_macros == False:
            file_writer.write('\n\n')
            for key in macro_count_dict:
    	       	file_writer.write("{} = {}".format(key, macro_count_dict[key]) + '\n')
            file_writer.write('\nTotal count is : ' + str(count))
            create_xls_file(macro_count_dict)
        else:
            for element in macros_all_set:
                macros_handle.write(element + '\n')    

