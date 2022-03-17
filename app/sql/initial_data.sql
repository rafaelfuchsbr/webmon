INSERT INTO public.website(website_id, name, url, regex, status)
VALUES 
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf61', 'HTTP STATUS 200', 'https://httpstat.us/200',	'200',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf62', 'HTTP STATUS 201', 'https://httpstat.us/201',	'ERROR',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf63', 'HTTP STATUS 202', 'https://httpstat.us/202',	'202',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf64', 'HTTP STATUS 203', 'https://httpstat.us/203',	'203',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf65', 'HTTP STATUS 204', 'https://httpstat.us/204',	'204',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf66', 'HTTP STATUS 300', 'https://httpstat.us/300',	'300',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf67', 'HTTP STATUS 302', 'https://httpstat.us/302',	'ERROR',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf68', 'HTTP STATUS 304', 'https://httpstat.us/304',	'304',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf69', 'HTTP STATUS 400', 'https://httpstat.us/400',	'400',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf60', 'HTTP STATUS 401', 'https://httpstat.us/401',	'401',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf10', 'HTTP STATUS 402', 'https://httpstat.us/402',	'ERROR',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf11', 'HTTP STATUS 403', 'https://httpstat.us/403',	'403',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf12', 'HTTP STATUS 404', 'https://httpstat.us/404',	'404',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf13', 'HTTP STATUS 405', 'https://httpstat.us/405',	'405',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf14', 'HTTP STATUS 500', 'https://httpstat.us/500',	'500',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf15', 'HTTP STATUS 502', 'https://httpstat.us/502',	'ERROR',	'active'),
('b3b1fa38-a32c-11eb-8d4f-163fd67fbf16', 'HTTP STATUS 503', 'https://httpstat.us/503',	'503',	'active')
ON CONFLICT DO NOTHING;