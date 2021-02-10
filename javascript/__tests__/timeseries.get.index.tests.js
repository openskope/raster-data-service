const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When the time resolution is index, time zero is not specified, and second through fourth bands are requested", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'GET',
		    path: timeseriesServiceBase + '/timeseries/annual_5x5x5_dataset/uint16_variable?longitude=-123.0&latitude=45.0&timeResolution=index&start=1&end=3'
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });

    it ('Series range start and end should match the request', async function() {
        expect(response.entity.start).toEqual( "1" );
        expect(response.entity.end).toEqual( "3" );
    });

    it ('Series range startIndex and endIndex should match the request', async function() {
        expect(response.entity.startIndex).toEqual( 1 );
        expect(response.entity.endIndex).toEqual( 3 );
    });
    
    it ('Values should be an array with one element for the first pixel of each band', async function() {
        expect(response.entity.values).toEqual( [200,300,400] );
    });
});
