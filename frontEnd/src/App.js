import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';

class App extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      imageURL: '',
      uploadedFileName:''
    };

    this.handleUploadImage = this.handleUploadImage.bind(this);
    this.handleDownloadClick = this.handleDownloadClick.bind(this);

  }

  // const [uploadedFileName, setUploadedFileName] = useState(null);


  handleUploadImage(ev) {
    ev.preventDefault();

    const data = new FormData();
    data.append('file', this.uploadInput.files[0]);
    data.append('filename', this.fileName.value);

    // this.setState({ uploadedFileName: this.fileName.value });
    

    fetch('http://localhost:4567/upload', {
      method: 'POST',
      body: data,
    }).then((response) => {
      response.json().then((body) => {
        console.log("filename:",this.fileName.value);
        console.log("files0:",this.uploadInput.files[0].name);

        this.setState({ imageURL: `http://localhost:4567/${body.file}`,
        uploadedFileName: this.uploadInput.files[0].name });
      });
    });
  }

  handleDownloadClick = (ev) => {
    // const filename = 'SQL.pdf'; // 你要下载的文件名
    const { imageURL, uploadedFileName } = this.state;

    const filename = `${uploadedFileName.split('.')[0]}_result.zip`;

    // 使用Fetch API进行文件下载
    fetch(`http://localhost:4567/download/${filename}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob();
      })
      .then((blob) => {
        // 创建一个临时的URL对象
        const url = URL.createObjectURL(blob);

        // 创建一个虚拟的a标签进行下载
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();

        // 清除临时的URL对象
        URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error('Error during file download:', error);
      });
  };

  render() {
    return (
      <form onSubmit={this.handleUploadImage}>
        <div>
          <input ref={(ref) => { this.uploadInput = ref; }} type="file" />
          <button>Upload</button>
        </div>
        {/* <div>
          <input ref={(ref) => { this.fileName = ref; }} type="text" placeholder="Enter the desired name of file" />
        </div> */}
        <br />
        {/* <div>
        </div> */}
        <div>
          <button onClick={this.handleDownloadClick}>下载文件</button>
        </div>
        {/* <img src={this.state.imageURL} alt="img" /> */}
      </form>
    );
  }
}

export default App;
