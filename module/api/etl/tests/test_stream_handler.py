#! /usr/bin/env python
# -*- coding: utf-8 -*-

from etl import stream_handler


def test_serialize():

    handler = stream_handler.StreamHandler()

    row = ["2021-02-16 00:42:19", "0.2126"]
  
    expected_dict = {'date' : "2021-02-16 00:42:19", 'sentiment' : "0.2126"}

    assert expected_dict == handler.serialize(row)