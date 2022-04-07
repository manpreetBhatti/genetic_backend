import React, { Component } from 'react';
import '../css/App.css';
import NavBar from '../js/NavBar';
import DetailsForm from '../js/DetailsForm';

class App extends Component {
  render() {
    return (
     	<div className="app-main">
     		<div className="nav-bar">
     			<NavBar></NavBar> 
     		</div>
     		<div className="form-container">
     			<DetailsForm/>
     		</div>
      	</div>
    );
  }
}

export default App;