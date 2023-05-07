import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios'
import { Table } from 'react-bootstrap';
import Button from 'react-bootstrap/Button'
import { b64ToBlob } from '../App';
import { useParams } from 'react-router-dom';


function ViewCandidateDetails() {

  const {id} = useParams()
  
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/candidate-detail/'+id+'/', {
      headers: {
        'Accept': 'application/json'
      }
    })
      .then(response => {
        setData(response.data);
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });

  }, [id]);

  return (
    <div className='container' style={{backgroundColor: '#FFFFFF', height: '100vh'}}>
      <h1 style={{textAlign: 'center'}}>user</h1>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>ID</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Email</th>
              <th>Description</th>
              {/* <th>CV</th> */}
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{data.id}</td>
              <td>{data.first_name}</td>
              <td>{data.last_name}</td>
              <td>{data.email}</td>
              <td>{data.description}</td>
            </tr>
          </tbody>
        </Table>
        <div className="text-center">
          <object data={b64ToBlob(data.cv)} type="application/pdf" width="100%" height="500px"></object>
        </div>
        <div className="text-center m-3">
          <Button  variant="primary" size="lg">
            <a style={{color: 'white', textDecoration:"none"}} href={b64ToBlob(data.cv)} download> Download CV</a>
          </Button>
        </div>
    </div>
  );
}

export default ViewCandidateDetails;