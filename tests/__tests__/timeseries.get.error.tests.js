const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a values GET request is missing the longitude parameter", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?latitude=45.0&start=0&end=4'
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });

    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that longitude parameter is not present', async function() {
        expect(response.entity.message).toBe("Required String parameter 'longitude' is not present");
    });    
});

describe("When a values GET request is missing the lat parameter", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-123.0&start=0&end=4'
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });

    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that longitude parameter is not present', async function() {
        expect(response.entity.message).toBe("Required String parameter 'latitude' is not present");
    });    
});

describe("When a values GET request specifies coordinates outside of raster file", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-124.0&latitude=45.0&start=0&end=4'
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

describe("When a values GET request specifies a dataset that does not exist", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/not-a-dataset/uint16_variable?longitude=-123.0&latitude=45.0&start=0&end=4'
		});
    });

    it ('HTTP response status code should be 400 - bad request', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that dataset file does not exist', async function() {
        expect(response.entity.message).toBe("Data file for dataset 'not-a-dataset', variable 'uint16_variable' does not exist on timeseries server.");
    });
    
});

describe("When a values GET request specifies a nonexistent variable for dataset", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/not-a-variable?longitude=-123.0&latitude=45.0&start=0&end=4'
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
    
});

describe("When a values GET request specifies a range start outside of dataset coverage", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-123.0&latitude=45.0&start=5&end=5'
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
    
});

describe("When a values GET request specifies a range end outside of dataset coverage", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-123.0&latitude=45.0&start=3&end=5'
		});
    });
	
    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should represent bands from the first band through the actual end band', async function() {
        expect(response.entity.start).toEqual( "3" );
        expect(response.entity.end).toEqual( "4" );
    });

    it ('Values should be an array with one element for the first requested band through the last actual band', async function() {
        expect(response.entity.values).toEqual( [400,500] );
    });
    
});

describe("When a values GET request specifies a range end before range start", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-123.0&latitude=45.0&start=4&end=3'
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
    
});
