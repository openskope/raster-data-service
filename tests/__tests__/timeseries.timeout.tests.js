const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a GET request specifies a timeout shorter than required when requesting a point geometry", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-123.0&latitude=45.0&start=0&end=4&timeout=1'
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that external process timed out', async function() {
        expect(response.entity.message).toMatch(new RegExp("External process exceeded time limit of 1 milliseconds:"));
    }); 
});

describe("When a POST request specifies in the query line a timeout shorter than required when requesting a polygon geometry", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries?timeout=1',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123,45],
	    		        [-123,47],
	    		        [-121,47],
	    		        [-121,45],
	    		        [-123,45]
	    		    	]]
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

    it ('Error message should be that external process timed out', async function() {
        expect(response.entity.message).toMatch(new RegExp("External process exceeded time limit of 1 milliseconds:"));
    }); 
});

describe("When a POST request specifies in the body a timeout shorter than required when requesting a polygon geometry", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123,45],
	    		        [-123,47],
	    		        [-121,47],
	    		        [-121,45],
	    		        [-123,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4,
	    		timeout: 1
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that external process timed out', async function() {
        expect(response.entity.message).toMatch(new RegExp("External process exceeded time limit of 1 milliseconds:"));
    }); 
});
