from flask import *
import urllib.request

app: Flask = Flask(__name__)
parse: bool = False
courses: dict = {}

with urllib.request.urlopen("http://time-table.sicsr.ac.in/day.php") as response:
    for line in response.read().decode("UTF-8").splitlines():
        line: str = line.strip()
        if parse:
            if line == "</select>":
                break
            else:
                tag: list = line.split('value="')[1].split('">')
                courses[str(tag[1]).split("</option>")[0].strip()] = tag[0]
        elif line == '<select id="type" name="type">':
            parse = True


def get_sicsr_course_classes(course_name: str, courses: dict) -> list:
    classes: list = []
    index: int = 0
    with urllib.request.urlopen(urllib.request.Request("http://time-table.sicsr.ac.in/day.php",
                                                       f"type={courses[course_name]}&submit=Submit".encode("UTF-8"))) as parent_response:
        for parent_line in parent_response.read().decode("UTF-8").splitlines():
            parent_line: str = parent_line.strip()
            if (parent_line.startswith('<a href="view')):
                classes.append(dict())
                index = len(classes)-1
                with urllib.request.urlopen(
                    f"""http://time-table.sicsr.ac.in/{
                    parent_line.split('<a href="')[1].split('"')[0].strip().replace("amp;", "")
                        }""") as child_response:

                    child_lines: list = list(
                        str(line).strip() for line in child_response.read().decode("UTF-8").splitlines())

                    for i in range(0, len(child_lines)):
                        child_lines[i]: str = child_lines[i].strip()

                        if (str(child_lines[i]).endswith("</h3>")):
                            classes[index]["Class"] = str(
                                child_lines[i]).rstrip("</h3>")

                        elif (str(child_lines[i]).startswith('<td>SICSR -')):
                            classes[index]["Room"] = str(
                                child_lines[i]).lstrip('<td>SICSR -').rstrip('</td>').strip()

                        elif (str(child_lines[i]) == "<td>Start time:</td>"):
                            classes[index]["Start Time"] = str(
                                child_lines[i+1]).lstrip('<td>').rstrip('</td>').split('-')[0].strip()

                        elif (str(child_lines[i]) == "<td>End time:</td>"):
                            classes[index]["End Time"] = str(
                                child_lines[i+1]).lstrip("<td>").rstrip("</td>").split('-')[0].strip()
    return classes

@app.route("/", methods=['GET', 'POST'])
def index():
    classes: list = []
    index: int = 0
    if (request.method == "POST" and request.form.get("submit") == "Submit"):
        with urllib.request.urlopen(urllib.request.Request("http://time-table.sicsr.ac.in/day.php",
                                                       f"type={courses[request.form.get('type')]}&submit=Submit".encode("UTF-8"))) as parent_response:
            for parent_line in parent_response.read().decode("UTF-8").splitlines():
                parent_line: str = parent_line.strip()
                if (parent_line.startswith('<a href="view')):
                    classes.append(dict())
                    index = len(classes)-1
                    with urllib.request.urlopen(
                        f"""http://time-table.sicsr.ac.in/{
                        parent_line.split('<a href="')[1].split('"')[0].strip().replace("amp;", "")
                            }""") as child_response:

                        child_lines: list = list(
                            str(line).strip() for line in child_response.read().decode("UTF-8").splitlines())

                        for i in range(0, len(child_lines)):
                            child_lines[i]: str = child_lines[i].strip()

                            if (str(child_lines[i]).endswith("</h3>")):
                                classes[index]["Class"] = str(
                                    child_lines[i]).rstrip("</h3>")

                            elif (str(child_lines[i]).startswith('<td>SICSR -')):
                                classes[index]["Room"] = str(
                                    child_lines[i]).lstrip('<td>SICSR -').rstrip('</td>').strip()

                            elif (str(child_lines[i]) == "<td>Start time:</td>"):
                                classes[index]["Start Time"] = str(
                                    child_lines[i+1]).lstrip('<td>').rstrip('</td>').split('-')[0].strip()

                            elif (str(child_lines[i]) == "<td>End time:</td>"):
                                classes[index]["End Time"] = str(
                                    child_lines[i+1]).lstrip("<td>").rstrip("</td>").split('-')[0].strip()
        return "\n".join(["""
<script>
    if ( window.history.replaceState ) {
        window.history.replaceState( null, null, window.location.href );
    }
</script>
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    td,
    tr,
    table {
        font-size: xx-large;
        margin: 1vh;                  
        padding: 1vh;
    }
</style>
<div style=" 
margin: 0;
position: absolute;
top: 50%;
left:50%;
-ms-transform: translate(-50%, -50%);
transform: translate(-50%, -50%);
                          margin:auto">
<table border="1">
<tr>
    <td>Class</td>
    <td>Room</td>
    <td>Start Time</td>
    <td>End Time</td>
</tr>"""]+[f"""<tr>
<td>{i["Class"]}</td>
<td>{i["Room"]}</td>
<td>{i["Start Time"]}</td>
<td>{i["End Time"]}</td>
</tr>""" for i in classes] + ["""</table>
<center>
<button style="padding:1vh; font-size: xx-large;" onClick="window.location.href=window.location.href">Back</button>
</center></div>"""])
    else:
        return """<div style=" 
margin: 0;
position: absolute;
top: 50%;
left:50%;
-ms-transform: translate(-50%, -50%);
transform: translate(-50%, -50%);">
<form method="post" action="/">
<select style="padding: 1vh; font-size: xx-large" id="type" name="type">
<option>BCA (V) - Div. A</option>
<option>BCA (V) - Div. B</option>
<option>BCA (V) - Div. C</option>
<option>BCA (V) - Div. D</option>
<option>BCA (V) - Div. E</option>
<option>BCA (V) - Elective</option>
<option>BCA (III) - Div. A</option>
<option>BCA (III) - Div. B</option>
<option>BCA (III) - Div. C</option>
<option>BCA (III) - Div. D</option>
<option>BCA (III) - Div. E</option>
<option>BCA (III) - Div. F</option>
<option>BCA(Honours) (V) - Elective</option>
<option>BCA(Honours) (III) - Elective</option>
<option>BBA-IT (V) - Div. A</option>
<option>BBA-IT (V) - Div. B</option>
<option>BBA-IT (V) - Div. C</option>
<option>BBA-IT (V) - Elective</option>
<option>BBA-IT (III) - Div. A</option>
<option>BBA-IT (III) - Div. B</option>
<option>BBA-IT (III) - Div. C</option>
<option>BBA-IT (III) - Elective</option>
<option>BBA-IT(Honours) (III) - Elective</option>
<option>MSC-CA (I)</option>
<option>MSC-CA (III)</option>
<option>MSC-CA (III) - SD</option>
<option>MSC-CA (III) - DS</option>
<option>MBA-DT (I)</option>
<option>MBA-DT (III)</option>
<option>MBA-IT (I) - Div. A</option>
<option>MBA-IT (I) - Div. B</option>
<option>MBA-IT (III)</option>
<option>MBA-IT (III) - DA</option>
<option>MBA-IT (III) - ITIM</option>
<option>Meetups/Placement</option>
<option>EXAM</option>
<option>Elective</option>
<option>Common Batch</option>
<option>Guest Lecture</option>
<option>BBA-IT (I) - Div. A</option>
<option>BBA-IT (I) - Div. B</option>
<option>BBA-IT (I) - Div. C</option>
<option>BREAK</option>
<option>BCA (I) - Div. A</option>
<option>BCA (I) - Div. B</option>
<option>BCA (I) - Div. C</option>
<option>BCA (I) - Div. D</option>
<option>BCA (I) - Div. E</option>
<option>BCA (I) - Div. F</option>
<option>type.x</option>
<option>type.y</option>
<option>type.z</option>
</select>
<input style="padding: 1vh; font-size: xx-large" type="submit" value="Submit" name="submit">
</form>
"""

if __name__ == "__main__":
    app.run()