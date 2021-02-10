const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a values POST request is missing the datasetId property", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });

    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that datasetId property is not present', async function() {
        expect(response.entity.message).toBe("Required property 'datasetId' is not present");
    });    
});

describe("When a values POST request is missing the variableName property", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });

    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that variableName property is not present', async function() {
        expect(response.entity.message).toBe("Required property 'variableName' is not present");
    });    
});

describe("When a values POST request is missing the boundaryGeometry property", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });

    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that latitude property is not present', async function() {
        expect(response.entity.message).toBe("Required property 'latitude' is not present");
    });    
});

describe("When a values POST request specifies an unsupported boundary geometry type", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'NoSuchGeometry',
		    		coordinates: [-123, 45]
		    	},		    	
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });

    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that value for boundaryGeometry.type property is not supported', async function() {
        expect(response.entity.message).toBe("'NoSuchGeometry' is not a supported value for property 'boundaryGeometry.type'");
    });    
});

describe("When a values POST request specifies coordinates outside of raster file", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-124, 45]
		    	},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400 - bad request', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that coordinates are outside dataset coverage', async function() {
        expect(response.entity.message).toBe("Coordinates are outside region covered by the dataset");
    });
    
});

describe("When a values POST request specifies a dataset that does not exist", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'not-a-dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400 - bad request', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that dataset file does not exist', async function() {
        expect(response.entity.message).toBe( "Data file for dataset 'not-a-dataset', variable 'uint16_variable' does not exist on timeseries server.");
    });
    
});

describe("When a values POST request specifies a nonexistent variable for dataset", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'not-a-variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400 - bad request', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that dataset file does not exist', async function() {
        expect(response.entity.message).toBe("Data file for dataset 'annual_5x5x5_dataset', variable 'not-a-variable' does not exist on timeseries server.");
    });
    
})

describe("When a values POST request specifies a range start outside of dataset coverage", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 5,
	    		end: 5
		    }
		});
    });

    it ('HTTP response status code should be 400 - bad request', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that range start is outside dataset coverage', async function() {
        expect(response.entity.message).toBe("Time range start is outside coverage of dataset");
    });
    
})

describe("When a values POST request specifies a range end outside of dataset coverage", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 3,
	    		end: 5
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should represent bands from the first band through the requested end band', async function() {
        expect(response.entity.start).toEqual( "3" );
        expect(response.entity.end).toEqual( "4" );
    });

    it ('Values should be an array with one element for the first band through the requested end band', async function() {
        expect(response.entity.values).toEqual( [400,500] );
    });
    
})


describe("When a values POST request specifies a range end before range start", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
		    		type: 'Point',
		    		coordinates: [-123, 45]
		    	},
	    		start: 4,
	    		end: 3
		    }
		});
    });

    it ('HTTP response status code should be 400 - bad request', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that range end precedes range start', async function() {
        expect(response.entity.message).toBe("Time range end is before time range start");
    });
    
})