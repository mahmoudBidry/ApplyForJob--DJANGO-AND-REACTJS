import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios'
import { Table } from 'react-bootstrap';
import Button from 'react-bootstrap/Button'
import {b64ToBlob} from '../App'
import { Link } from "react-router-dom";
import { Modal, useModal, Text } from "@nextui-org/react";




function ViewCandidates() {

  const { setVisible, bindings } = useModal(false);
  

  const [data, setData] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [prepareDelete, setPrepareDelete] = useState(false)
  const [transactionState, setTransactionState] = useState({
    message : "",
    color : ""
  })

  const filteredData = data.filter((item) => {
    const fullName = `${item.first_name} ${item.last_name} ${item.email} ${item.description}`.toLowerCase();
    return fullName.includes(searchQuery.toLowerCase());
  });
  
  const deleteUser = async (userId) => {
    const options = {
      url: 'http://localhost:8000/api/candidate-delete/'+userId+'/',
      method: 'DELETE',
      headers: {
        'Accept': 'application/json'
      }
    };
    axios(options)
      .then(response => {
        getUsers();
        if (response.status === 204) {
          setVisible(true);
          setTransactionState({
            message : "Candidate deleted successfully",
            color : "success"
          });
        }
      })
      .catch(error => {
        if (error.response.status !== 204) {
          setVisible(true);
          setTransactionState({
            message : error.response.data?.message,
            color : "error"
          });
        }      
      });
  }
  

  const getUsers = async () =>{
    const options = {
      url: 'http://localhost:8000/api/candidate-list/',
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    };
    axios(options)
      .then(response => {
        setData(
          response.data.map(item => {
            return {...item, cv_blob: b64ToBlob(item.cv) };
          })
        )
      })
      .catch(error => {
        console.error("error a: ",error);
      });
  }

  useEffect(() => {
    getUsers();
  }, []);

  return (
    <div className='container' style={{backgroundColor: '#FFFFFF', height: '100vh'}}>
      <h1 style={{textAlign: 'center'}}>All users</h1>
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
            
            <Button onClick={() => setVisible(false)}>
              Agree
            </Button>
          </Modal.Footer>
        </Modal>
      </div>
      {data.length > 0 && (
        <div>
          <input type="text" placeholder="Search for a user" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} />
          <br/>
          <br/>
          <Table bordered hover>
            <thead>
              <tr>
                <th>ID</th>
                <th>First Name</th>
                <th>Last Name</th>
                <th>Email</th>
                <th>Description</th>
                <th>CV</th>
                <th>View details</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item, index) => (
                <tr key={index}>
                  <td>{item.id}</td>
                  
                  <td>{item.first_name}</td>
                  <td>{item.last_name}</td>
                  <td>{item.email}</td>
                  <td>{item.description}</td>
                  <td>
                    <div className='d-flex justify-content-center'>
                    
                      <Button  variant="success" size="sm">
                        <a style={{color: 'white', fontSize : "15px", textDecoration:"none"}} href={item.cv_blob} target="_blank" rel="noreferrer">
                          View CV
                        </a>
                      </Button>
                    </div>
                  </td>
                  <td>
                    <div className='d-flex justify-content-center'>
                      <Button  variant="info" size="sm">
                        <Link to={`/ViewCandidateDetails/${item.id}`} style={{color:"white", fontSize : "15px", textDecoration:"none"}}>View Details</Link>                  
                      </Button>
                    </div>
                  </td>
                  <td>
                      <div className='d-flex justify-content-center'>
                        {!prepareDelete && (
                          <Button variant="danger" size="sm" onClick={() => setPrepareDelete(true)}    >
                          Delete 
                        </Button>
                        ) }

                        {prepareDelete && (
                          <Button variant="danger" size="sm" 
                                onClick={async() =>{
                                  await deleteUser(item.id)
                                  setPrepareDelete(false)
                                }}
                        >
                          Confirm 
                        </Button>
                        ) }
                        
                      </div>
                  </td>
                </tr>
              ))}
              
            </tbody>
          </Table>
        </div>
      )}
      
    </div>
  );
}

export default ViewCandidates;