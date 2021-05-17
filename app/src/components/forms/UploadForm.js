import React, { Component } from 'react';
import classnames from 'classnames';
import axios from 'axios';

class UploadForm extends Component {
  constructor(props) {
    super(props);
    this.state = { username: '', selectedFile: null };
  }

  onFileChange = (event) => {
    this.setState({ selectedFile: event.target.files[0] });
    console.log(5555555555);
  };

  onFileUpload = () => {
    const formData = new FormData();
    const { selectedFile, username } = this.state;

    formData.append('username', username);
    formData.append('filename', selectedFile.name);
    formData.append('file', selectedFile);

    // Details of the uploaded file
    console.log(selectedFile);

    // Request made to the backend api
    // Send formData object
    axios.post('http://localhost:5000/file_upload/', JSON.stringify(formData));
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
            type="file"
            name="filename"
            onChange={this.onFileChange}
          />
          <input
            className="input"
            type="text"
            name="username"
            placeholder="Your username"
          />
        </div>
        <div className="control">
          <button
            className="button button-primary button-block button-shadow"
            type="submit"
            onClick={(event) => {
              event.preventDefault();
              this.onFileUpload();
            }}
          >
            {submit}
          </button>
        </div>
      </form>
    );
  }
}

export default UploadForm;
