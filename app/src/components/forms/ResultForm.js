import React, { Component } from 'react';
import classnames from 'classnames';
import { URLSearchParams } from 'url';

class ResultForm extends Component {
  constructor(props) {
    super(props);
    this.state = { username: '', selectedFile: null };
  }

  onNameChange = (event) => {
    const { username} = this.state;
    user = username.input()
    fileSelect = null;

    const params = { username: username.value };

    fetch(
      'http://localhost:5000/get_file_list/?' + new URLSearchParams(params)
    ).then(function (response) {
      response.json().then(function (data) {
        let optionHTML = '';
        for (let file of data.files) {
          optionHTML +=
            '<option value="' + file.id + '">' + file.name + '</option>';
        }
        file_select.innerHTML = optionHTML;
      });
    });
  };

  onFileChange = (event) => {
    this.setState({ selectedFile: event.target.files[0] });
  };

  onDisplay = () => {
    const formData = new FormData();
    const { selectedFile, username } = this.state;

    formData.append('username', username);
    formData.append('filename', selectedFile.name);

    // Details of the uploaded file
    console.log(selectedFile);

    // Request made to the backend api
    // Send formData object
    axios.get('http://localhost:5000/file_upload/', JSON.stringify(formData));
  };

  render() {
    const { className, submit = 'Submit' } = this.props;
    const { username, selectedFile } = this.state;

    return (
      <form
        className={classnames(
          'newsletter-form field field-grouped is-revealing',
          className
        )}
        onSubmit={this.onFileUpload}
      >
        <div className="control control-expanded">
          <input
            className="input"
            type="text"
            name="username"
            placeholder="Your username"
          />
          <input
            className="select"
            type="select"
            name="filename"
            onChange={this.onFileChange}
          />
        </div>
        <div className="control">
          <button
            className="button button-primary button-block button-shadow"
            type="submit"
            onClick={(event) => {
              event.preventDefault();
              this.onDisplay();
            }}
          >
            {submit}
          </button>
        </div>
      </form>
    );
  }
}

export default ResultForm;
