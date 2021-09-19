# -*- coding:utf-8 -*-
#!/usr/bin/env python
"""
Date: 2020/10/12 18:16
Desc: To test intention, just write test code here!
"""
from akshare.cost.cost_living import cost_living


def test_cost_living():
    """
    just for test aim
    :return: assert result
    :rtype: assert
    """
    cost_living_df = cost_living()
    assert cost_living_df.shape[0] > 0


if __name__ == "__main__":
    test_cost_living()
