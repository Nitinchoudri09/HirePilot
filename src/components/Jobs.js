import React, { useEffect, useState } from "react";
import { fetchJobs } from "../api/jobs";

const Jobs = () => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    fetchJobs().then(setJobs);
  }, []);

  return (
    <div>
      <h1>Latest Jobs</h1>

      {jobs.map((job, index) => (
        <div key={index}>
          <h2>{job.job_title}</h2>

          <p>{job.employer_name}</p>

          <a href={job.job_apply_link}>
            Apply
          </a>
        </div>
      ))}
    </div>
  );
};

export default Jobs;
