import React, { Component } from 'react';
import '../css/App.css';
import { Form, Button, Spinner, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';


class DetailsForm extends Component {

	constructor(props) {
    	super(props);
    	this.state = {
    		email: "",
    		inputNeurons: "",
    		outputNeuron: "",
    		file: "",
    		processing: false,
    		api_done: false,
    		success: true
    	};

    	this.updateEmail = this.updateEmail.bind(this);
    	this.updateInput = this.updateInput.bind(this);
    	this.updateOutput = this.updateOutput.bind(this);
    	this.updateFile = this.updateFile.bind(this);
    	this.submitFile = this.submitFile.bind(this);
    	this.processResponse = this.processResponse.bind(this);
  	}

  	updateEmail(event){
  		this.setState({
  			emailId: event.target.value
  		})
  	}

  	updateInput(event){
  		this.setState({
  			inputNeurons: event.target.value
  		})
  	}

  	updateOutput(event){
  		this.setState({
  			outputNeuron: event.target.value
  		})
  	}

  	updateFile(event){
  		this.setState({
  			file: event.target.files[0]
  		})
  	}

  
	submitFile(event){
		event.preventDefault();
		var formData = new FormData();
		for ( var key in this.state ) {
		    formData.append(key, this.state[key]);
		}
		this.setState({
  			processing: true
  		})
  		var this_ = this;
		axios({
		  method: "post",
		  url: "http://127.0.01:5000/data",
		  data: formData,
		  headers: { "Content-Type": "multipart/form-data" }
		})
        .then(response => this.processResponse(response.data))
        .catch(function(error){
        	this_.setState({
	  			processing: false,
	  			api_done: true,
	  			success: false
	  		})
        });
  	}

  	processResponse(data)
  	{
  		this.setState({
  			processing: false,
  			api_done: true,
  			success: true,
  		})
  	}	

  	render() {
  		let form = <Form onSubmit={this.submitFile}>
						<Form.Group controlId="formBasicEmail">
							<Form.Label>Email address</Form.Label>
							<Form.Control type="email" placeholder="Enter email" required value={this.state.emailId} onChange={this.updateEmail}/>
						</Form.Group>

						<Form.Group controlId="formBasicInput">
							<Form.Label>Number of Input Neurons</Form.Label>
							<Form.Control type="number" placeholder="Number of Input Neurons" required value={this.state.inputNeurons} onChange={this.updateInput} min="2"/>
						</Form.Group>
						<Form.Group controlId="formBasicClasses">
							<Form.Label>Number of Classes</Form.Label>
							<Form.Control type="number" placeholder="Number of Classes" required value={this.state.outputNeuron} onChange={this.updateOutput} min="2"/>
						</Form.Group>
						<Form.Group controlId="formBasicInputFile">
							<Form.Label>Train Dataset Upload</Form.Label>
							<Form.Control type="file" placeholder="Dataset upload" required onChange={this.updateFile}/>
						</Form.Group>
						<Button variant="primary" type="submit" >
							Submit
						</Button>
				</Form>
		let spinner = <div style={{textAlign:'center'}}>
						<Spinner animation="border" role="status">
					  	<span className="sr-only">Loading...</span>
						</Spinner>
					</div>
		let alert = <Alert variant="success">
					  <Alert.Heading>Data Successfully Uploaded!</Alert.Heading>
					  <p>
					  	We have recieved your data and have started looking for the best neural network architecture that suits your needs!
					  </p>
					  <p>
					  	We will send over the details of the neural network as email since the process may take upto couple of hours.
					  </p>
					</Alert>

		let alert_failed = 	<Alert variant="danger">
							  <Alert.Heading>Uh Oh!</Alert.Heading>
							  <p>
							  	We are facing issues! Try adjusting the parameters!
							  </p>
							</Alert>		

		var container = <div></div>

		if(this.state.processing)
		{
			container = spinner
		}
		else
		{
			if(this.state.api_done)
			{
				container = this.state.success?alert:alert_failed
			}
			else
			{
				container = form
			}
		}	

	    return (
	     	<div>
				{container}				
			</div>
	    );
	  }
}

export default DetailsForm;