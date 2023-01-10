const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const input = document.querySelector('#input_selector');
const output = document.querySelector('#output_selector');
const file_input = document.querySelector('#file_input');

async function getFormats() {

    let request = new Request(
        "",
        {headers: {'X-CSRFToken': csrftoken}}
    );

    let response = await fetch(request, {
         method: 'POST',
         mode: 'same-origin',
    });

    let formats = await response.json();

    console.log(formats)

    let input_html = input.innerHTML;
    for (let file_group in formats) {
        input_html += "<optgroup label="+file_group+">";
        for (let format in formats[file_group]) {
            option = '<option ' + 'value="' + file_group + ":" + format + '">' + format + '</option>'
            input_html += option;
        }
        input_html += "</optgroup>";
    }


    input.innerHTML = input_html;

    let output_html = output.innerHTML;

     async function inputChanged() {
        splited_value = input.value.split(":")

        selected_format = splited_value[1];
        selected_group = splited_value[0];

        console.log(selected_group, selected_format)

        selected_output = formats[selected_group][selected_format]

        let new_output_html = output_html;

        for (let i = 0; i < selected_output.length; i++) {
            let format = selected_output[i]
            new_output_html += '<option>' + format.split(" ")[0] + '</option>';
        }
        output.innerHTML = new_output_html;
    }

    input.addEventListener('change', inputChanged);

    file_input.addEventListener('change', async function() {
        input_file = file_input.value;
        splited = input_file.split(".");
        input_file_format = splited[splited.length - 1];

        let changed = false
        for (let file_group in formats) {
            for (let file_type in formats[file_group]){
                if (file_type.includes(input_file_format)){
                    input.value = file_group + ":" +file_type;
                    inputChanged();
                    changed = true
                    break
                }
            }
            if (changed){break;}
        }
        if (!changed){
            alert("Unsupported file format: " + input_file_format);
            file_input.value = ""
        }
    });
}
getFormats();