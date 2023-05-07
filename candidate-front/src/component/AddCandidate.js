import React, { useState } from 'react';
import { useFormik } from 'formik'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal, useModal, Button, Text } from "@nextui-org/react";



function AddCandidate() {
  const { setVisible, bindings } = useModal(false);
  const [file, setFile] = useState({
    file: null,
  });
  const [transactionState, setTransactionState] = useState({
    message : "",
    color : ""
  })

  const formik = useFormik({
    initialValues: {
      firstName: '',
      lastName: '',
      email: '',
      description: ''
    },
    onSubmit: values => {
      saveFormData(values);
    },
    validate: values => {
      let errors = {};
      if (!values.firstName)
        errors.firstName = 'Required';
      if (!values.lastName)
        errors.lastName = 'Required';
      if (!values.email)
        errors.email = 'Required';
      if (!values.description)
        errors.description = 'Required';
      return errors;
    }
  })

  const handleChangeFile = (e) => {
      setFile(e.target.files[0]);
  };

  


  const saveFormData = (formData) => {
    const formDataWithFile = new FormData();
    formDataWithFile.append('first_name', formik.values.firstName);
    formDataWithFile.append('last_name', formik.values.lastName);
    formDataWithFile.append('email', formik.values.email);
    formDataWithFile.append('description', formik.values.description);
    formDataWithFile.append('cv', file);
    
    const options = {
      url: 'http://localhost:8000/api/candidate-create/',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
      },
      data: formDataWithFile
    };

    axios(options)
      .then(response => {
        if (response.status === 201) {
          setVisible(true);
          setTransactionState({
            message : response.data.message,
            color : "success"
          });
        }
      })
      .catch(error => {
        if (error.response.status === 400) {
          setVisible(true);
          setTransactionState({
            message : error.response.data.message,
            color : "error"
          });
        }
      });
  };

  return (
    <div className='container'>
      <div>
        <Modal
          scroll
          width="600px"
          aria-labelledby="modal-title"
          aria-describedby="modal-description"
          {...bindings}
        >
          <Modal.Header>
            <Text id="modal-title" size={18}>
              State
            </Text>
          </Modal.Header>
          <Modal.Body>
            <Text id="modal-description" color={transactionState.color}>
              {transactionState.message}
            </Text>
          </Modal.Body>
          <Modal.Footer>
            
            <Button auto onPress={() => setVisible(false)}>
              Agree
            </Button>
          </Modal.Footer>
        </Modal>
      </div>

      <form onSubmit={formik.handleSubmit} className="container">
        <div className="form-group">
          <label htmlFor="firstName">First Name</label>
          <input
            type="text"
            name="firstName"
            value={formik.values.name}
            onChange={formik.handleChange}
            placeholder="Name"
            className='form-control'
          />
          {formik.errors.firstName ? <div className='error'>{formik.errors.firstName}</div> : null}
        </div>
        <div className="form-group">
          <label htmlFor="lastName">Last Name</label>
          <input
            type="text"
            name="lastName"
            value={formik.values.lastName}
            onChange={formik.handleChange}
            placeholder="Last Name"
            className='form-control'
          />
           {formik.errors.lastName ? <div className='error'>{formik.errors.lastName}</div> : null}
        </div>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            name="email"
            value={formik.values.email}
            onChange={formik.handleChange}
            placeholder="Email"
            className='form-control'
          />
          {formik.errors.email ? <div className='error'>{formik.errors.email}</div> : null}
        </div>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            name="description"
            value={formik.values.description}
            onChange={formik.handleChange}
            placeholder="Description"
            className='form-control'
          />
          {formik.errors.description ? <div className='error'>{formik.errors.description}</div> : null}
        </div>
        <div className="form-group">
          <label htmlFor="file">CV</label>
          <input
            type="file"
            name="file"
            onChange={handleChangeFile}
            className='form-control'
          />
        </div>
        <button className='btn btn-primary mt-3' style={{ width: '100%' }} type="submit">Submit</button>
      </form>
    </div>
  );
}

export default AddCandidate;